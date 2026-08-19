"""
MTProto File chunking and partitioning.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import BinaryIO

CHUNK_SIZE_SMALL = 128 * 1024  # 128 KB
CHUNK_SIZE_BIG = 512 * 1024  # 512 KB
BIG_FILE_THRESHOLD = 10 * 1024 * 1024  # 10 MB


def get_chunk_size(file_size: int) -> int:
    """
    Get recommended chunk size for file transfer.
    """
    if file_size > BIG_FILE_THRESHOLD:
        return CHUNK_SIZE_BIG
    return CHUNK_SIZE_SMALL


def chunk_bytes(data: bytes, chunk_size: int) -> Generator[tuple[int, bytes], None, None]:
    """
    Yields (part_index, chunk_data) from in-memory byte buffer.
    """
    for index, offset in enumerate(range(0, len(data), chunk_size)):
        yield index, data[offset : offset + chunk_size]


def chunk_file(file_obj: BinaryIO, chunk_size: int) -> Generator[tuple[int, bytes], None, None]:
    """
    Yields (part_index, chunk_data) by reading file in chunks.
    """
    index = 0
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        yield index, chunk
        index += 1
