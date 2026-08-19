"""
Diffie-Hellman and Pollard's rho PQ factorization for MTProto handshake.
"""

from __future__ import annotations

import math
import os
import random
from typing import Tuple


def factorize_pq(pq: int) -> tuple[int, int]:
    """
    Decomposes pq into prime factors p and q such that p < q using Brent's cycle finding algorithm.

    :param pq: Product of two primes (typically 64-bit integer).
    :return: (p, q) with p < q.
    """
    if pq % 2 == 0:
        return 2, pq // 2

    # Brent's variant of Pollard's rho
    for _ in range(100):
        y = random.randint(1, pq - 1)
        c = random.randint(1, pq - 1)
        m = 128
        g, r, q = 1, 1, 1
        ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (pow(y, 2, pq) + c) % pq
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (pow(y, 2, pq) + c) % pq
                    q = (q * abs(x - y)) % pq
                g = math.gcd(q, pq)
                k += m
            r *= 2

        if g == pq:
            while True:
                ys = (pow(ys, 2, pq) + c) % pq
                g = math.gcd(abs(x - ys), pq)
                if g > 1:
                    break

        if 1 < g < pq:
            p = g
            q_val = pq // p
            return (p, q_val) if p < q_val else (q_val, p)

    msg = f"Failed to factorize pq={pq}"
    raise ValueError(msg)


def check_dh_params(dh_prime: int, g: int) -> bool:
    """
    Validate DH prime and generator.
    """
    if g not in (2, 3, 4, 5, 6, 7):
        return False
    # Ensure prime is 2048 bits
    if dh_prime.bit_length() < 2040 or dh_prime.bit_length() > 2048:
        return False
    return True


def check_dh_g(g_a: int, dh_prime: int) -> bool:
    """
    Validate that g_a or g_b satisfies Telegram's security bounds.
    """
    min_val = 1 << (2048 - 64)
    max_val = dh_prime - min_val
    return min_val <= g_a <= max_val


def generate_dh_b(dh_prime: int, g: int) -> tuple[int, int]:
    """
    Generate client DH secret exponent b and public value g_b = (g^b) mod dh_prime.

    :param dh_prime: 2048-bit prime integer.
    :param g: Generator integer.
    :return: (b, g_b).
    """
    # 2048-bit random exponent b
    b_bytes = os.urandom(256)
    b = int.from_bytes(b_bytes, "big") % (dh_prime - 1)
    if b <= 1:
        b += 2
    g_b = pow(g, b, dh_prime)
    return b, g_b


def compute_auth_key(g_a: int, b: int, dh_prime: int) -> bytes:
    """
    Compute MTProto 256-byte AuthKey from server public value g_a and client secret b:
    auth_key = (g_a ^ b) mod dh_prime.

    :param g_a: Server public DH value.
    :param b: Client secret DH exponent.
    :param dh_prime: 2048-bit prime.
    :return: 256-byte AuthKey.
    """
    key_int = pow(g_a, b, dh_prime)
    return key_int.to_bytes(256, "big")
