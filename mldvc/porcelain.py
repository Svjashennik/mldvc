import os
import pathlib
import typing as tp

from mldvc.index import read_index, update_index
from mldvc.objects import commit_parse, find_object, find_tree_files, read_object
from mldvc.refs import get_ref, is_detached, resolve_head, update_ref
from mldvc.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    for path in paths:
        if not path.is_dir():
            update_index(gitdir, [path], write=True)
        else:
            add(gitdir, list(path.glob("*")))


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    parent_commit = resolve_head(gitdir)
    commit_hash = commit_tree(gitdir, tree, message, parent_commit, author)
    return commit_hash


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    ...
