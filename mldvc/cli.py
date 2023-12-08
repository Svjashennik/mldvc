import argparse

from mldvc.index import ls_files, read_index, update_index
from mldvc.objects import cat_file, hash_object
from mldvc.porcelain import checkout, commit
from mldvc.refs import ref_resolve, symbolic_ref, update_ref
from mldvc.repo import repo_create, repo_find
from mldvc.tree import commit_tree, write_tree


def cmd_init(args: argparse.Namespace):
    # TODO: Reinitialized existing pyvcs repository
    gitdir = repo_create(args.path)
    print(f"Initialized empty pyvcs repository in {gitdir.absolute()}")


def cmd_hash_object(args: argparse.Namespace):
    with args.path.open(mode="rb") as f:
        data = f.read()

    sha = hash_object(data, args.type, args.write)
    print(sha)


def cmd_cat_file(args: argparse.Namespace):
    cat_file(args.object, args.pretty)


def cmd_ls_files(args: argparse.Namespace):
    gitdir = repo_find()
    ls_files(gitdir, details=args.stage)


def cmd_update_index(args: argparse.Namespace):
    gitdir = repo_find()
    update_index(gitdir, args.paths, write=args.add)


def cmd_write_tree(args: argparse.Namespace):
    gitdir = repo_find()
    entries = read_index(gitdir)
    sha = write_tree(gitdir, entries)
    print(sha)


def cmd_commit_tree(args: argparse.Namespace):
    gitdir = repo_find()
    sha = commit_tree(gitdir, args.tree, args.message, args.parent)
    print(sha)


def cmd_update_ref(args: argparse.Namespace):
    gitdir = repo_find()
    update_ref(gitdir, args.ref, args.newvalue)


def cmd_rev_parse(args: argparse.Namespace):
    gitdir = repo_find()
    sha = ref_resolve(gitdir, args.rev)
    print(sha)


def cmd_symbolic_ref(args: argparse.Namespace):
    gitdir = repo_find()
    symbolic_ref(gitdir, args.name, args.ref)


def cmd_commit(args: argparse.Namespace):
    gitdir = repo_find()
    sha = commit(gitdir, args.message, args.author)
    print(sha)


def cmd_checkout(args: argparse.Namespace):
    gitdir = repo_find()
    checkout(gitdir, args.obj_name)
