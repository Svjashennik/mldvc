import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from mldvc.objects import hash_object

PACK_FORMAT = '>10L20sH'
FILE_NAME_FORMAT = 's3x'


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
        return struct.pack(PACK_FORMAT + f'{self.flags}{FILE_NAME_FORMAT}', *packing_data)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        values = struct.unpack(PACK_FORMAT, data[: struct.calcsize(PACK_FORMAT)])
        name = struct.unpack_from(f'{values[-1]}{FILE_NAME_FORMAT}', data, 62)[0].decode()
        return GitIndexEntry(*values, name)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index_list = []
    try:
        with open(gitdir / 'index', 'rb') as file:
            index_data = file.read()
            index = struct.unpack('>4s2L', index_data[:12])
            start = 12
            for _ in range(index[2]):
                limit = start + struct.calcsize(PACK_FORMAT)
                data = index_data[start:limit]
                init_row = struct.unpack(PACK_FORMAT, data)
                data += index_data[limit : limit + init_row[-1] + 3]
                index_list.append(GitIndexEntry.unpack(data))
                start += len(data)
    except FileNotFoundError:
        pass
    return index_list


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / 'index', 'wb') as index:
        index.write(struct.pack('>4s2L', 'DIRC'.encode(), 2, len(entries)))
        for entry in entries:
            index.write(entry.pack())


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    index = read_index(gitdir)
    for gitindex in index:
        if details:
            print(f'{format(gitindex.mode, "o")} {gitindex.sha1.hex()} 0  {gitindex.name}')
        else:
            print(gitindex.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    for path in paths:
        stat = os.stat(path)
        with open(path, 'rb') as file:
            data = file.read()
        entries.append(
            GitIndexEntry(
                int(stat.st_ctime),
                0,
                int(stat.st_mtime),
                0,
                stat.st_dev,
                stat.st_ino,
                stat.st_mode,
                stat.st_uid,
                stat.st_gid,
                stat.st_size,
                bytes.fromhex(hash_object(data, 'blob', write=True)),
                len(str(path)),
                str(path),
            )
        )
    if write:
        write_index(gitdir, entries)
