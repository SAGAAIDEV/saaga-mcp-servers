"""
Redis client utility for direct Redis operations.
"""

import os
import redis
from typing import Any, Optional, Union
from saaga_mcp_base.config.env import REDIS


class RedisClient:
    """
    Redis client for direct Redis operations.
    """

    def __init__(self, url: Optional[str] = None):
        """
        Initialize Redis client.

        Args:
            url: Redis URL. If None, uses REDIS.URL environment variable or default.
        """
        self.redis_url = url or REDIS.URL
        self.client = redis.from_url(self.redis_url)

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis.

        Args:
            key: Redis key
            value: Value to store
            ex: Expiration time in seconds

        Returns:
            bool: True if successful
        """
        return self.client.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[bytes]:
        """
        Get a value from Redis.

        Args:
            key: Redis key

        Returns:
            Optional[bytes]: Value or None if key doesn't exist
        """
        return self.client.get(key)

    def delete(self, key: str) -> int:
        """
        Delete a key from Redis.

        Args:
            key: Redis key

        Returns:
            int: Number of keys deleted
        """
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        Args:
            key: Redis key

        Returns:
            bool: True if key exists
        """
        return bool(self.client.exists(key))

    def publish(self, channel: str, message: str) -> int:
        """
        Publish a message to a Redis channel.

        Args:
            channel: Channel name
            message: Message to publish

        Returns:
            int: Number of clients that received the message
        """
        return self.client.publish(channel, message)

    def subscribe(self, channel: str) -> None:
        """
        Subscribe to a Redis channel.

        Args:
            channel: Channel name
        """
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub


# Singleton instance for easy import
redis_client = RedisClient()
