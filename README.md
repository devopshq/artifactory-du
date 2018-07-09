Artifactory Disk Usage cli (artifactory-du)
==========================================

[![docs](https://img.shields.io/readthedocs/pip.svg)](https://devopshq.github.io/artifactory-du/)  [![dohq build status](https://travis-ci.org/devopshq/artifactory-du.svg)](https://travis-ci.org/devopshq/artifactory-du) [![dohq on PyPI](https://img.shields.io/pypi/v/dohq-artifactory-du.svg)](https://pypi.python.org/pypi/dohq-artifactory-du) [![dohq-artifactory-du license](https://img.shields.io/pypi/l/vspheretools.svg)](https://github.com/devopshq/artifactory-du/blob/master/LICENSE)

`artifactory-du` - estimate file space usage

Summarize disk usage in JFrog Artifactory of the set of FILEs, recursively for directories.

# Table of Contents
TODO

# Install
```cmd
# Install from PyPi
python -mpip install artifactory-du

# and try get help
artifactory-du --help
```

# Usage
You can use `artifactory-du` like original *nix `du`, but you need use some specific option (see `artifactory-du --help` for describe)
```cmd
# Recursive summary for all folder in repo.snapshot
artifactory-du --username username --password password --artifactory-url https://repo.example.ru/artifactory --repository repo.snapshot -h -s *

# Set alias for linux
alias adu=artifactory-du --username username --password password --artifactory-url https://repo.example.ru/artifactory --repository repo.snapshot -h
# usage
adu --max-depth=2 /*

# Set alias for Windows
set "adu=artifactory-du --username username --password password --artifactory-url https://repo.example.ru/artifactory --repository repo.snapshot -h"
# usage
%adu% --max-depth=2 /*

```

Below we miss artifactory-specific options: `username, password, artifactory-url, repository`, because we use ALIAS (for [linux-bash](https://askubuntu.com/questions/17536/how-do-i-create-a-permanent-bash-alias) or [windows-cmd](https://superuser.com/a/560558)

```cmd
# Summary for subfolder in foldername
adu --max-depth=2 folder/*

# show 2 folder level inside repository
adu --max-depth=2 *

# Show only directory with GB size
adu --max-depth=0 * | grep G

# Show artifacts that have never been downloaded
adu --max-depth=0 * --without-downloads | grep G

# Show artifacts that older than 30 days
adu --max-depth=0 * --older-than 30 | grep G

```

## Artifactory options
### Connection
- `--artifactory-url http://arti.example.com/artifactory` -URL to artifactory, e.g: https://arti.example.com/artifactory"
- `--username USERNAME` - user how have READ access to repository
- `--password PASSWORD`, - user's password how have READ access to repository
- `--repository REPOSITORY` - Specify repository
- `--verbose` - increase output verbosity

### Specific
- `--without-downloads` - Find items that have never been downloaded (`stat.downloads == 0`)
- `--older-than DAY_COUNT` - counts for files older than `DAY_COUNT`

## du common options support
- `--max-depth N` - print the total for a directory (or file, with --all) only if it is N or fewer levels below the command line argument; `--max-depth=0` is the same  as `--summarize`
- `--human-readable, -h` - print sizes in human readable format (e.g., 1K 234M 2G)
- `--all` - write counts for all files, not just directories
- `--summarize` - display only a total for each argument

# Known issue
1. Does not support filename in `<file>`: `artifactory-du -h -s */*.deb` will fail
2. Does not print folder if `summarize` folder: `artifactory-du -h -s foldername` will out: `123G    /` , expected as original `du`: `123G    foldername`


---------------
Inspired by https://github.com/reversefold/artifactory-disk-usage
