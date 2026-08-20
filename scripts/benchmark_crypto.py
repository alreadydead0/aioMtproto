import os
import time

from aiogram.mtproto.crypto.aes_ige import aes_ige_decrypt, aes_ige_encrypt


def run_benchmark() -> None:
    key, iv = os.urandom(32), os.urandom(32)
    data = os.urandom(10 * 1024 * 1024)

    start = time.perf_counter()
    for _ in range(10):
        aes_ige_encrypt(data, key, iv)
    elapsed = time.perf_counter() - start
    print(f"Encrypt Throughput: {100 / elapsed:.1f} MB/s")

    start = time.perf_counter()
    for _ in range(10):
        aes_ige_decrypt(data, key, iv)
    elapsed = time.perf_counter() - start
    print(f"Decrypt Throughput: {100 / elapsed:.1f} MB/s")


if __name__ == "__main__":
    run_benchmark()
