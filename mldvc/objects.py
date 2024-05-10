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
    tree = []
    while data:
        start_sha = data.index(b"\00")
        mode_b: bytes
        name_b: bytes
        mode_b, name_b = data[:start_sha].split(b" ")
        mode = mode_b.decode()
        name = name_b.decode()
        sha = data[start_sha + 1 : start_sha + 21]
        tree.append((int(mode), name, sha.hex()))
        data = data[start_sha + 21 :]
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    objects = resolve_object(obj_name, gitdir)
    for object_name in objects:
        if pretty:
            fmt, content = read_object(object_name, gitdir)
            if fmt in ['blob', 'commit']:
                print(content.decode())
            else:
                for tree in read_tree(content):
                    if tree[0] != 40000:
                        print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])
                    else:
                        print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
        else:
            print(object_name)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    result: tp.Dict[str, tp.Any] = {"message": []}
    for i in map(lambda x: x.decode(), raw.split(b"\n")):
        if "tree" in i or "parent" in i or "author" in i or "committer" in i:
            name, val = i.split(" ", maxsplit=1)
            result[name] = val
        else:
            result["message"].append(i)
    return result
