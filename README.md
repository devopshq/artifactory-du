Artifactory Disk Usage cli (artifactory-du)
==========================================

[![docs](https://img.shields.io/readthedocs/pip.svg)](https://devopshq.github.io/artifactory-du/)  [![dohq build status](https://travis-ci.org/devopshq/artifactory-du.svg)](https://travis-ci.org/devopshq/artifactory-du) [![dohq on PyPI](https://img.shields.io/pypi/v/artifactory-du.svg)](https://pypi.python.org/pypi/artifactory-du) [![artifactory-du license](https://img.shields.io/pypi/l/vspheretools.svg)](https://github.com/devopshq/artifactory-du/blob/master/LICENSE)

`artifactory-du` - estimate file space usage

Summarize disk usage in JFrog Artifactory of the set of FILEs, recursively for directories.

# Table of Contents
- [Install](#install)
- [Usage](#usage)
    - [Artifactory options](#artifactory-options)
        - [Connection](#connection)
        - [Specific](#specific)
    - [DU options](#du-options)
- [Known issues](#known-issues)
- [CONTRIBUTING](#contributing)
- [AD](#ad)


# Install
```cmd
# Install from PyPi
python -mpip install artifactory-du

# and try get help
artifactory-du --help
```

# Usage
`artifactory-du` is used in the same manner as original `du` from *nix, although launch options are different. See artifactory-du --help for details.
```cmd
# Recursive summary for root folder in repo.snapshot
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

Below we skip artifactory-specific options: `username, password, artifactory-url, repository`, because we use ALIAS (for [linux-bash](https://askubuntu.com/questions/17536/how-do-i-create-a-permanent-bash-alias) or [windows-cmd](https://superuser.com/a/560558)

```cmd
# Summary for subfolder in folder
adu --max-depth=2 folder/*

# show 2 folder level inside repository
adu --max-depth=2 *

# Show only directory with GB size
adu --max-depth=0 * | grep G

# Show artifacts that have never been downloaded
adu --max-depth=0 * --without-downloads | grep G

# Show artifacts older than 30 days
adu --max-depth=0 * --older-than 30 | grep G

```

## Artifactory options
### Connection
- `--artifactory-url http://arti.example.com/artifactory` -URL to artifactory, e.g: https://arti.example.com/artifactory"
- `--username USERNAME` - user which has READ access to repository
- `--password PASSWORD`, - user's password which has READ access to repository
- `--repository REPOSITORY` - Specify repository
- `--verbose` - increase output verbosity

### Specific
- `--without-downloads` - Find items that have never been downloaded (`stat.downloads == 0`)
- `--older-than DAY_COUNT` - only counts size for files older than `DAY_COUNT`

## DU options
- `--max-depth N` - print the total size for a directory (or file, with --all) only if it is N or fewer levels below the command line argument; `--max-depth=0` is the same  as `--summarize`
- `--human-readable, -h` - print sizes in human readable format (e.g., 1K 234M 2G)
- `--all` - write counts for all files, not just directories
- `--summarize` - display only a total for each argument

# Known issues
1. Does not support filename in `<file>`: `artifactory-du -h -s */*.deb` will fail
2. Does not print folder if `summarize` folder: `artifactory-du -h -s foldername` will out: `123G    /` , expected as original `du`: `123G    foldername`

# CONTRIBUTING
Contributing:
- Create your own github-fork
- Change files
- Create pull request to `develop`-branch

Create release:
- Dump version on `develop`-branch in `artifactory_du.version.py`
- Pull request to `master`
- Profit :)

# AD
We also have python-script for Artifactory intelligence cleanup rules with config format like this:
```python
GOOD_FILTER_PATH_SYMBOLS = [
    r'*release*', r'*/r-*',
    r'*master*',
    r'*stable*',
]

RULES = [
    {'name': 'Clean all *.tmp',
     'rules': [
         rules.repo_by_mask('*.tmp'),
         rules.delete_older_than_n_days(7),
     ]},

    {'name': 'Clean all *.BANNED after 7 days',
     'rules': [
         rules.repo_by_mask('*.BANNED'),
         rules.delete_older_than_n_days(7),
     ]},

    {'name': 'Clean all *.snapshot after 30 days',
     'rules': [
         rules.repo_by_mask('*.snapshot'),
         rules.delete_older_than_n_days(30),
     ]},

     {'name': 'tech-symbols',
     'rules': [
         rules.repo, # repo-name like 'name'
         rules.delete_older_than_n_days(30),
         rules.filter_without_path_mask(GOOD_FILTER_PATH_SYMBOLS),
         rules.filter_without_filename_mask(GOOD_FILTER_PATH_SYMBOLS),
         rules.filter_by_filename_mask('*-*symbols.tar.gz'),
         rules.without_downloads()
     ]},

     {'name': 'docker-scmdev',
     'rules': [
         rules.repo, # repo-name like 'name'
         rules.filter_by_path_mask('scmdev.test*'),
         rules.delete_images_older_than_n_days(1),
     ]},
]

```

If you want it, please vote for issue and we will schedule time for move project to open-source: https://github.com/devopshq/artifactory-du/issues/2


---------------
Inspired by https://github.com/reversefold/artifactory-disk-usage
