import subprocess
from typing import Dict, Optional, List

# Removed urllib.parse as it's not directly used here now; REDIS/FLOWER configs are handled in start.py
# from urllib.parse import urlparse

# Import service starting functions from start.py
# Assuming start.py is in a location accessible by this import path.
# If start.py is in the same directory, the import might need adjustment based on Python's path resolution.
# For now, let's assume it's structured as a module.
from saaga_mcp_base.lib.scheduler.core.processes import (
    start_redis,
    start_celery_worker,
    start_celery_beat,
    start_flower,
)
from saaga_mcp_base.lib.logging import logger

# We might need to import REDIS and FLOWER config if we want to pass specific ports
# derived from them, or override start.py's defaults. For now, rely on start.py's defaults.
# from src.config.env import REDIS, FLOWER


# To store Popen objects for started processes
managed_processes: Dict[str, subprocess.Popen] = {}

# TODO: Add a restart function


async def start_scheduler_services(
    redis_port: Optional[int] = None,  # Allow overriding default port from REDIS.URL
    worker_concurrency: int = 4,
    flower_port: Optional[int] = None,  # Allow overriding default port from FLOWER.PORT
) -> Dict[str, str]:
    """
    Starts Redis, Celery worker, Celery beat, and Flower.
    Services are started in non-daemonized mode to be managed by this script.
    Args:
        redis_port: Optional port for Redis.
        worker_concurrency: Concurrency for the Celery worker.
        flower_port: Optional port for Flower.
    Returns:
        A dictionary with the status of each attempted start.
    """
    results = {}

    # Start Redis
    if "redis" in managed_processes and managed_processes["redis"].poll() is None:
        logger.info("Redis is already running and managed.")
        results["redis"] = "already_running"
    else:
        logger.info(
            f"Starting Redis... (Port: {redis_port or 'default from REDIS.URL'})"
        )
        process = start_redis(port=redis_port, daemonize=False)
        if process:
            managed_processes["redis"] = process
            results["redis"] = f"started (PID: {process.pid})"
            logger.info(f"Redis started with PID: {process.pid}")
        else:
            results["redis"] = "failed_to_start_or_daemonized_unexpectedly"
            logger.info(
                "Redis process was not returned, check its start logic for non-daemonized mode."
            )

    # Start Celery Worker
    if (
        "celery_worker" in managed_processes
        and managed_processes["celery_worker"].poll() is None
    ):
        logger.info("Celery worker is already running and managed.")
        results["celery_worker"] = "already_running"
    else:
        logger.info(f"Starting Celery worker with concurrency {worker_concurrency}...")
        process = start_celery_worker(concurrency=worker_concurrency)
        managed_processes["celery_worker"] = process
        results["celery_worker"] = f"started (PID: {process.pid})"
        logger.info(f"Celery worker started with PID: {process.pid}")

    # Start Celery Beat
    if (
        "celery_beat" in managed_processes
        and managed_processes["celery_beat"].poll() is None
    ):
        logger.info("Celery beat is already running and managed.")
        results["celery_beat"] = "already_running"
    else:
        logger.info("Starting Celery beat for scheduled tasks...")
        process = start_celery_beat()
        managed_processes["celery_beat"] = process
        results["celery_beat"] = f"started (PID: {process.pid})"
        logger.info(f"Celery beat started with PID: {process.pid}")

    # Start Flower
    if "flower" in managed_processes and managed_processes["flower"].poll() is None:
        logger.info("Flower is already running and managed.")
        results["flower"] = "already_running"
    else:
        logger.info(
            f"Starting Flower... (Port: {flower_port or 'default from FLOWER.PORT'})"
        )
        process = start_flower(port=flower_port, daemonize=False)
        managed_processes["flower"] = process
        results["flower"] = f"started (PID: {process.pid})"
        logger.info(f"Flower started with PID: {process.pid}")

    return results


async def stop_scheduler_services() -> Dict[str, str]:
    """
    Stops all managed services (Redis, Celery worker, Celery beat, Flower).
    Returns:
        A dictionary with the status of each stop attempt.
    """
    results = {}
    for name, process in list(
        managed_processes.items()
    ):  # Iterate over a copy for safe deletion
        if process.poll() is None:  # Check if process is running
            logger.info(f"Stopping {name} (PID: {process.pid})...")
            process.terminate()
            try:
                process.wait(
                    timeout=10
                )  # Increased timeout for potentially slower services
                logger.info(f"{name} stopped.")
                results[name] = "stopped"
            except subprocess.TimeoutExpired:
                logger.info(f"{name} did not terminate in time, killing...")
                process.kill()
                process.wait()  # Wait for kill to complete
                logger.info(f"{name} killed.")
                results[name] = "killed"
            del managed_processes[name]
        else:
            logger.info(
                f"{name} was not running or already stopped (Return Code: {process.returncode})."
            )
            results[name] = (
                f"already_stopped_or_not_running (code: {process.returncode})"
            )
            if (
                name in managed_processes
            ):  # Ensure it's removed if already stopped but still in dict
                del managed_processes[name]

    if not results:
        logger.info("No services were actively managed or running to stop.")
        return {"status": "no_active_services_to_stop"}

    return results


async def get_services_status() -> Dict[str, str]:
    """
    Gets the status of all potentially managed services.
    Cleans up entries for processes that have terminated.
    """
    status = {}
    service_names = ["redis", "celery_worker", "celery_beat", "flower"]

    for name in service_names:
        if name in managed_processes:
            process = managed_processes[name]
            if process.poll() is None:
                status[name] = f"running (PID: {process.pid})"
            else:
                status[name] = f"stopped (Return Code: {process.returncode})"
                # Clean up if stopped
                del managed_processes[name]
        else:
            status[name] = "not_managed_or_stopped"

    if not status:
        return {"status": "no_services_currently_managed"}

    return status


# Old functions like start_celery_worker, start_celery_beat, start_celery, stop_celery
# are removed as their functionality is now part of start_all_services and stop_all_services.
