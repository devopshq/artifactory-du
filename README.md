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
```
Below we miss artifactory-specific options: `username, password, artifactory-url, repository`

```cmd
# Summary for subfolder in foldername
artifactory-du -h --max-depth=2 folder/*

# show 2 folder level inside repository
artifactory-du -h --max-depth=2 *
```

## Artifactory specific options
- `--artifactory-url` -URL to artifactory, e.g: https://arti.example.com/artifactory"
- `--username` - user how have READ access to repository
- `--password`, - user's password how have READ access to repository
- `--repository` - Specify repository
- `--verbose` - increase output verbosity

## du common options support
- `--human-readable, -h` - print sizes in human readable format (e.g., 1K 234M 2G)
- `--max-depth` - print the total for a directory (or file, with --all) only if it is N or fewer levels below the command line argument; `--max-depth=0` is the same  as `--summarize`
- `--all` - write counts for all files, not just directories
- `--summarize` - display only a total for each argument

# Known issue
1. Does not support filename in `<file>`: `artifactory-du -h -s */*.deb` will fail
2. Does not print folder if `summarize` folder: `artifactory-du -h -s foldername` will out: `123G    /` , expected as original `du`: `123G    foldername`


---------------
Inspired by https://github.com/reversefold/artifactory-disk-usage
