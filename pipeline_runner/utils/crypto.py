"""Cryptographic utility functions."""
import hashlib
import hmac
import os


def hash_value(value, algorithm="sha256"):
    """Hash a string value using the specified algorithm."""
    h = hashlib.new(algorithm)
    h.update(value.encode("utf-8"))
    return h.hexdigest()


def generate_salt(length=32):
    """Generate a cryptographically secure random salt."""
    return os.urandom(length).hex()


def constant_time_compare(a, b):
    """Compare two strings in constant time to prevent timing attacks."""
    return hmac.compare_digest(
        a.encode("utf-8") if isinstance(a, str) else a,
        b.encode("utf-8") if isinstance(b, str) else b,
    )
