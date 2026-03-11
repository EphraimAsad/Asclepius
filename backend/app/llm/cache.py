"""
In-memory LRU cache with TTL for LLM responses.

Caches enhancement results to avoid redundant LLM calls for
identical symptom/rule combinations.
"""

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass
from threading import Lock
from typing import Any

from .base import EnhancedResult


@dataclass
class CacheEntry:
    """A cached enhancement result with timestamp."""
    result: EnhancedResult
    created_at: float


class LLMCache:
    """Thread-safe LRU cache with TTL for LLM responses.

    Args:
        max_size: Maximum number of entries (default 1000)
        ttl_seconds: Time-to-live for entries in seconds (default 3600 = 1 hour)
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._lock = Lock()
        self._hits = 0
        self._misses = 0

    @staticmethod
    def make_key(
        matched_rules: list[str],
        chief_complaint: str,
        symptoms: dict[str, Any]
    ) -> str:
        """Generate a cache key from the relevant context.

        The key is based on the rules that matched and symptoms,
        since the same rule matches should produce the same enhancement.
        """
        key_parts = [
            str(sorted(matched_rules)),
            chief_complaint,
            str(sorted((k, v) for k, v in symptoms.items() if v))
        ]
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]

    def get(self, key: str) -> EnhancedResult | None:
        """Get a cached result if it exists and hasn't expired.

        Args:
            key: Cache key from make_key()

        Returns:
            Cached EnhancedResult or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            entry = self._cache[key]

            # Check if expired
            if time.time() - entry.created_at > self._ttl_seconds:
                del self._cache[key]
                self._misses += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._hits += 1

            # Return a copy with from_cache flag set
            result = entry.result
            return EnhancedResult(
                enhanced_explanation=result.enhanced_explanation,
                follow_up_questions=result.follow_up_questions.copy(),
                from_cache=True
            )

    def set(self, key: str, result: EnhancedResult) -> None:
        """Store a result in the cache.

        Args:
            key: Cache key from make_key()
            result: The EnhancedResult to cache
        """
        with self._lock:
            # Remove oldest entries if at capacity
            while len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)

            self._cache[key] = CacheEntry(
                result=result,
                created_at=time.time()
            )

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0.0
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(hit_rate, 3),
                "ttl_seconds": self._ttl_seconds
            }

    def cleanup_expired(self) -> int:
        """Remove all expired entries.

        Returns:
            Number of entries removed
        """
        now = time.time()
        removed = 0

        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if now - entry.created_at > self._ttl_seconds
            ]
            for key in expired_keys:
                del self._cache[key]
                removed += 1

        return removed


# Global cache instance
_cache: LLMCache | None = None


def get_cache(max_size: int = 1000, ttl_seconds: int = 3600) -> LLMCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = LLMCache(max_size=max_size, ttl_seconds=ttl_seconds)
    return _cache


def reset_cache() -> None:
    """Reset the global cache (for testing)."""
    global _cache
    if _cache is not None:
        _cache.clear()
    _cache = None
