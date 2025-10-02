#!/usr/bin/env python3
"""
Generate a secure secret key for Flask applications.
Run this script to get a new secret key for your APP_SECRET_KEY environment variable.
"""

import secrets

def generate_secret_key():
    """Generate a secure 32-byte (256-bit) secret key"""
    return secrets.token_hex(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Flask Secret Key:")
    print(secret_key)
    print()
    print("Use this value for your APP_SECRET_KEY environment variable in Render.")
    print("Example:")
    print(f"APP_SECRET_KEY={secret_key}")
