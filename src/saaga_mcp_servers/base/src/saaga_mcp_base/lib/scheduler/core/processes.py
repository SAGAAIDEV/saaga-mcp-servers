#!/usr/bin/env python
"""
Utility script to start Redis, Celery, and Flower.
"""
import argparse
import os
import subprocess
import sys
import time
from typing import List, Optional
from saaga_mcp_base.config.env import REDIS, FLOWER
from urllib.parse import urlparse

# TODO: I think all the start functions should be factored out to seperate files


def start_redis(port: int = None, daemonize: bool = True) -> Optional[subprocess.Popen]:
    """
    Start a Redis server.

    Args:
        port: Redis port (defaults to port from REDIS.URL if None)
        daemonize: Run Redis as a daemon

    Returns:
        Optional[subprocess.Popen]: Process object if not daemonized
    """
    # Extract port from REDIS.URL if not provided
    if port is None:
        try:
            # Parse the Redis URL to extract the port
            parsed_url = urlparse(REDIS.URL)
            port = parsed_url.port or 6379
        except Exception:
            port = 6379

    print(f"Starting Redis on port {port}...")

    cmd = ["redis-server", "--port", str(port)]
    if daemonize:
        cmd.append("--daemonize yes")
        subprocess.run(cmd, check=True)
        return None
    else:
        process = subprocess.Popen(cmd)
        time.sleep(1)  # Give Redis time to start
        return process


def start_celery_worker(
    concurrency: int = 4, loglevel: str = "INFO"
) -> subprocess.Popen:
    """
    Start a Celery worker.

    Args:
        concurrency: Number of worker processes
        loglevel: Log level

    Returns:
        subprocess.Popen: Process object
    """
    print(f"Starting Celery worker with concurrency {concurrency}...")

    cmd = [
        "celery",
        "-A",
        "saaga_mcp_base.lib.scheduler.core.celery_app",
        "worker",
        "--concurrency",
        str(concurrency),
        "--loglevel",
        loglevel,
    ]
    return subprocess.Popen(cmd)


def start_celery_beat() -> subprocess.Popen:
    """
    Start Celery beat for scheduled tasks.

    Returns:
        subprocess.Popen: Process object
    """
    print("Starting Celery beat for scheduled tasks...")

    cmd = [
        "celery",
        "-A",
        "saaga_mcp_base.lib.scheduler.core.celery_app",
        "beat",
        "--loglevel",
        "INFO",
    ]
    return subprocess.Popen(cmd)


def start_flower(
    port: Optional[int] = None, daemonize: bool = False
) -> subprocess.Popen:
    """
    Start Flower for monitoring.

    Args:
        port: Flower web UI port (defaults to FLOWER.PORT if None)

    Returns:
        subprocess.Popen: Process object
    """
    if port is None:
        port = FLOWER.PORT

    # Try to extract port from Redis URL for broker API
    broker_api_port = 6379  # Default Redis port
    try:
        parsed_url = urlparse(REDIS.URL)
        if parsed_url.port:
            broker_api_port = parsed_url.port
    except Exception:
        # If URL parsing fails, use default port
        pass

    # Build command
    cmd = [
        "celery",
        "-A",
        "saaga_mcp_base.lib.scheduler.core.celery_app",
        "flower",
        f"--port={port}",
        "--address=0.0.0.0",
        f"--broker_api=redis://localhost:{broker_api_port}/0",
        "--persistent=True",
        f"--db={FLOWER.DB}",
    ]

    # Add basic auth if configured
    if FLOWER.BASIC_AUTH:
        cmd.append(f"--basic_auth={FLOWER.BASIC_AUTH}")

    # Add daemonize flag if requested
    if daemonize:
        cmd.append("--daemonize")

    return subprocess.Popen(cmd)


# TODO: Factor this out to scheduler/cli.py and use google fire.
def main(args=None):
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Start scheduler components")
    parser.add_argument("--redis", action="store_true", help="Start Redis")
    parser.add_argument("--worker", action="store_true", help="Start Celery worker")
    parser.add_argument("--beat", action="store_true", help="Start Celery beat")
    parser.add_argument("--flower", action="store_true", help="Start Flower")
    parser.add_argument("--all", action="store_true", help="Start all components")

    # Get default Redis port from REDIS.URL if possible
    default_redis_port = 6379
    try:
        port_part = REDIS.URL.split(":")[2].split("/")[0]
        default_redis_port = int(port_part)
    except (IndexError, ValueError):
        pass

    # Default Flower port with fallback
    default_flower_port = getattr(FLOWER, "PORT", 5555)

    parser.add_argument(
        "--redis-port", type=int, default=default_redis_port, help="Redis port"
    )
    parser.add_argument(
        "--flower-port", type=int, default=default_flower_port, help="Flower port"
    )
    parser.add_argument("--concurrency", type=int, default=4, help="Worker concurrency")

    # For testing, we can pass in args directly
    parsed_args = parser.parse_args(args)

    processes: List[subprocess.Popen] = []

    try:
        # Determine what to start
        start_all = parsed_args.all
        start_redis_server = start_all or parsed_args.redis
        start_worker = start_all or parsed_args.worker
        start_beat = start_all or parsed_args.beat
        start_flower_server = start_all or parsed_args.flower

        # Start components
        if start_redis_server:
            redis_process = start_redis(port=parsed_args.redis_port, daemonize=False)
            if redis_process:
                processes.append(redis_process)

        if start_worker:
            worker_process = start_celery_worker(concurrency=parsed_args.concurrency)
            processes.append(worker_process)

        if start_beat:
            beat_process = start_celery_beat()
            processes.append(beat_process)

        if start_flower_server:
            flower_process = start_flower(port=parsed_args.flower_port)
            processes.append(flower_process)

        # Keep the script running
        print("All components started. Press Ctrl+C to stop.")
        for process in processes:
            process.wait()

    except KeyboardInterrupt:
        print("\nShutting down...")
        for process in processes:
            process.terminate()

        # Wait for processes to terminate
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        print("All components stopped.")


if __name__ == "__main__":  # pragma: no cover
    main()
