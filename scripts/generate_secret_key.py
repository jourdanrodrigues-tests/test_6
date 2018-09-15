#!/usr/bin/env python
from random import SystemRandom

if __name__ == '__main__':
    allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%^&*(-_=+)'
    system_random = SystemRandom()
    secret_key = ''.join([system_random.choice(allowed_chars) for _ in range(50)])
    print(secret_key)
