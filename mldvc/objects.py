import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from mldvc.refs import update_ref
from mldvc.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = fmt + f' {len(data)}\0'
    store = header.encode() + data
    hash_file = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find() / 'objects' / hash_file[:2]
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        with open(path / hash_file[2:], 'wb') as f:
            f.write(zlib.compress(store))
    return hash_file


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> list[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    header = obj_name[:2]
    index = obj_name[2:]
    obj_dir = gitdir / 'objects' / header
    for sub in obj_dir.iterdir():
        if sub.is_file() and sub.name.startswith(index):
            objects.append(header + sub.name)
    if not objects:
        raise Exception(f"Not a valid object name {obj_name}")
    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / 'objects' / sha[:2] / sha[2:]
    with open(path, mode="rb") as f:
        obj_data = zlib.decompress(f.read())
    delimiter = obj_data.find(b"\x00")
    header = obj_data[:delimiter][: obj_data.find(b' ')].decode()
    content = obj_data[delimiter + 1 :]
    return header, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    objects = resolve_object(obj_name, gitdir)
    for object_name in objects:
        if pretty:
            object_name = read_object(object_name, gitdir)[1].decode()
        print(object_name)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
