import os
import pathlib
from typing import Union

TYPE_FILE = 'file'
TYPE_DIR = 'dir'

REPO_STRUCTURE = {
    'HEAD': {'type': TYPE_FILE, 'init': 'ref: refs/heads/master\n'},
    'config': {
        'type': TYPE_FILE,
        'init': '[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n',
    },
    'description': {'type': TYPE_FILE, 'init': 'Unnamed mldvc repository.\n'},
    'objects': {'type': TYPE_DIR},
    'refs': {'type': TYPE_DIR, 'init': {'heads': {'type': TYPE_FILE}, 'tags': {'type': TYPE_FILE}}},
}


def repo_find(workdir: Union[str, pathlib.Path] = '.') -> pathlib.Path:
    # PUT YOUR CODE HERE
    ...


def repo_create(workdir: Union[str, pathlib.Path]) -> pathlib.Path:
    mldvc_dir = workdir / os.environ['MLDVC_DIR']
    try:
        os.mkdir(mldvc_dir)
    except Exception:
        raise Exception(f'{workdir} is not a directory')
    _create_structure(mldvc_dir, REPO_STRUCTURE)
    return mldvc_dir


def _create_structure(dir: Union[str, pathlib.Path], structure: dict):
    for name, data in structure.items():
        _create_file_or_dir(dir, name, data)


def _create_file_or_dir(dir: Union[str, pathlib.Path], name: str, data: dict):
    path = dir / name
    if data['type'] == TYPE_FILE:
        with open(path, 'w') as f:
            f.write(data.get('init', ''))
    elif data['type'] == TYPE_DIR:
        os.mkdir(path)
        _create_structure(path, data.get('init', {}))
