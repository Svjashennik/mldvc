import os
import pathlib
import stat
import time
import typing as tp

from mldvc.index import GitIndexEntry, read_index
from mldvc.objects import hash_object
from mldvc.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:

    data = ''
    for entry in index:
        data += f'{entry.mode} {entry.name}\0{entry.sha1}'
    hash_data = hash_object(data.encode(),'blob',write=True)
    return hash_data



def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
