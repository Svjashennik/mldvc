import os
import pathlib
import stat
import time
import typing as tp

from mldvc.index import GitIndexEntry, read_index
from mldvc.objects import hash_object
from mldvc.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    data = b''
    sub_dirs = {}
    for entry in index:
        path = entry.name.split('/')
        if len(path) == 1 or path[-2] == dirname:
            data += f'{entry.mode:o} {entry.name.split("/")[-1]}\0'.encode() + entry.sha1
        else:
            sub_dir = path[path.index(dirname) + 1] if dirname else path[0]
            if sub_dir not in sub_dirs:
                sub_dirs[sub_dir] = []
            sub_dirs[sub_dir].append(entry)
    for sub_dir in sorted(sub_dirs):
        hash_data = write_tree(gitdir, sub_dirs[sub_dir], sub_dir)
        data += f'040000 {sub_dir}\0'.encode() + bytes.fromhex(hash_data)
    hash_data = hash_object(data, 'tree', write=True)
    return hash_data


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: str | None,
    author: str | None,
) -> str:
    if author is None and 'GIT_AUTHOR_NAME' in os.environ and 'GIT_AUTHOR_EMAIL' in os.environ:
        author = f'{os.environ.get("GIT_AUTHOR_NAME")} <{os.environ.get("GIT_AUTHOR_EMAIL")}>'
    timezone = f'{"-" if time.timezone > 0 else "+"}{abs(time.timezone) // 60 // 60:02}{abs(time.timezone) // 60 % 60:02}'
    data = [f'tree {tree}']
    if parent is not None:
        data.append(f'parent {parent}')
    data.append(f'author {author} {int(time.mktime(time.localtime()))} {timezone}')
    data.append(f'committer {author} {int(time.mktime(time.localtime()))} {timezone}')
    data.append(f'\n{message}\n')
    return hash_object("\n".join(data).encode(), 'commit', write=True)
