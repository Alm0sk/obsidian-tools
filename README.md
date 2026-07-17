# obsidian-tool

CLI to sync a git-backed Obsidian vault: pull, signed commit, and push in one command.

## Requirements

- Python ≥ 3.9 and [pipx](https://pipx.pypa.io/)
- An Obsidian vault that is a git repository with a configured remote
- A GPG key configured for commit signing (`git commit -S`)

## Installation

```sh
pipx install git+ssh://git@github.com/Alm0sk/obsidian-tools.git
# or over HTTPS:
pipx install git+https://github.com/Alm0sk/obsidian-tools.git
# or from a local clone:
pipx install /path/to/obsidian-tools
```

Then set the vault location (in your shell profile):

```sh
export obsidian_vault_location=/path/to/your/vault
```

## Usage

```sh
obs pull              # git pull the vault
obs push              # git add -A, signed commit, push
obs sync              # pull, then commit + push
obs directory         # show the vault directory
obs push -m "message" # custom commit message
obs --help
```

Without `-m`, the commit message comes from `$obsidian_commit_message` if set, otherwise `vault backup: <date>`.

Exit codes: `0` on success, `1` if a git step fails, `2` on argument errors.

## Upgrading

```sh
pipx upgrade obsidian-tool
# or from a local clone:
pipx install --force /path/to/obsidian-tools
```
