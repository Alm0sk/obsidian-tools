#!/usr/bin/env python3
import argparse

import os
import subprocess
import sys
from datetime import datetime


def check_env_var():
    if os.getenv("obsidian_vault_location") is None:
        print("Error: The environment variable 'obsidian_vault_location' is not set.", file=sys.stderr)
        print("Please set: export obsidian_vault_location=/path/to/your/obsidian/vault", file=sys.stderr)
        sys.exit(1)

    if os.getenv("obsidian_commit_message") is None:
        default_message = f"vault backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        os.environ["obsidian_commit_message"] = default_message


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode == 0


def pull_vault(vault_location):
    print(f"Pulling vault from {vault_location} ...")
    if run(["git", "pull"], cwd=vault_location):
        print("Done!")
        return True
    print("Pull failed.", file=sys.stderr)
    return False


def commit_and_push_vault(vault_location, commit_message):
    print(f"Committing and pushing vault at {vault_location} ...")

    run(["git", "add", "-A"], cwd=vault_location)

    nothing_to_commit = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=vault_location
    ).returncode == 0
    if nothing_to_commit:
        print("Nothing to commit.")
        return True

    if not run(["git", "commit", "-S", "-m", commit_message], cwd=vault_location):
        print("Commit failed.", file=sys.stderr)
        return False

    if run(["git", "push"], cwd=vault_location):
        print("Done!")
        return True
    print("Push failed.", file=sys.stderr)
    return False


def build_parser():
    parser = argparse.ArgumentParser(
        prog="obsidian_tool",
        description="Sync an Obsidian vault backed by a git repository.",
    )
    parser.add_argument(
        "-m", "--message",
        help="Commit message to use (overrides $obsidian_commit_message and the auto-generated default).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("pull", help="Pull the vault from the remote.")
    subparsers.add_parser("push", help="Commit local changes and push the vault.")
    subparsers.add_parser("sync", help="Pull, then commit and push the vault.")
    subparsers.add_parser("directory", help="Show the vault directory.")

    return parser


def change_directory(vault_location):
    os.chdir(vault_location)
    return True

def main():
    parser = build_parser()
    args = parser.parse_args()

    check_env_var()
    vault_location = os.getenv("obsidian_vault_location")
    if args.message:
        os.environ["obsidian_commit_message"] = args.message
    commit_message = os.getenv("obsidian_commit_message")

    if args.command == "pull":
        ok = pull_vault(vault_location)
    elif args.command == "push":
        ok = commit_and_push_vault(vault_location, commit_message)
    elif args.command == "sync":
        ok = pull_vault(vault_location) and commit_and_push_vault(vault_location, commit_message)
    elif args.command == "directory":
        ok = change_directory(vault_location)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
