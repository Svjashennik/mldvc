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
    blob = fmt + f' {len(data)}\x00'
    store = blob.encode() + data
    hash_file = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find() / 'objects' / hash_file[:2]
        try:
            os.mkdir(path)
            with open(path / hash_file[2:], 'wb') as f:
                f.write(zlib.compress(store))
        except FileExistsError:
            pass
    return hash_file


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
