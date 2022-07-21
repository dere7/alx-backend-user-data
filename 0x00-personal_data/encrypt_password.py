#!/usr/bin/env python3
"""utils for hashing password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password for plain password"""
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """chdck hashed password matches one that has hashed"""
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False
