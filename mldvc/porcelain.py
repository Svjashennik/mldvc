import os
import pathlib
import typing as tp

from mldvc.index import read_index, update_index
from mldvc.objects import commit_parse, find_object, find_tree_files, read_object
from mldvc.refs import get_ref, is_detached, resolve_head, update_ref
from mldvc.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # PUT YOUR CODE HERE
    ...


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # PUT YOUR CODE HERE
    ...


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    ...
