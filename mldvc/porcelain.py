import os
import pathlib
import shutil
import typing as tp

from mldvc.index import read_index, update_index
from mldvc.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from mldvc.refs import get_ref, is_detached, resolve_head, update_ref
from mldvc.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, write=True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    parent_commit = resolve_head(gitdir)
    commit_hash = commit_tree(gitdir, tree, message, parent_commit, author)
    return commit_hash


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entry in read_index(gitdir):
        if pathlib.Path(entry.name).exists():
            os.remove(entry.name)
    commit_data = commit_parse(read_object(obj_name, gitdir)[1])
    while True:
        trees: list[tuple[list[tuple[int, str, str]], pathlib.Path]] = [
            (read_tree(read_object(commit_data["tree"], gitdir)[1]), gitdir.parent)
        ]
        while trees:
            tree_content, tree_path = trees.pop()
            for file_data in tree_content:
                fmt, data = read_object(file_data[2], gitdir)
                if fmt != "tree":
                    if not (tree_path / file_data[1]).exists():
                        with (tree_path / file_data[1]).open("wb") as file:
                            file.write(data)
                            (tree_path / file_data[1]).chmod(int(str(file_data[0]), 8))
                else:
                    if not (tree_path / file_data[1]).exists():
                        (tree_path / file_data[1]).mkdir()
                    trees.append((read_tree(data), tree_path / file_data[1]))
        if "parent" in commit_data:
            commit_data = commit_parse((read_object(commit_data["parent"], gitdir)[1]))
        else:
            break
    for dir in gitdir.parent.glob("*"):
        if dir.is_dir() and dir != gitdir:
            try:
                os.removedirs(dir)
            except OSError:
                continue
