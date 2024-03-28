import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from mldvc.objects import hash_object

PACK_FORMAT = '>10L20sH10s'


class GitIndexEntry(tp.NamedTuple):
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        packing_data = [value.encode() if isinstance(value, str) else value for value in self]
        return struct.pack(PACK_FORMAT, *packing_data)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        values = struct.unpack(PACK_FORMAT, data)
        return GitIndexEntry(*values[:-1], values[-1].decode().rstrip('\x00'))


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    ...


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
