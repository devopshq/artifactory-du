import argparse
import logging
import sys

import requests
from artifactory import ArtifactoryPath
from hurry.filesize import size

from du import out_as_du

requests.packages.urllib3.disable_warnings()


def init_logging():
    logger_format_string = '%(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logger_format_string, stream=sys.stdout)


def du(artifactory_url, username, password, repository, max_depth, file, human_readable, all):
    aql = ArtifactoryPath(artifactory_url, auth=(username, password), verify=False)
    aql_query_dict = {"repo": repository}
    if file:
        # Remove first / in path: /path => path
        file = file[1:] if file.startswith('/') else file
        if '*' in file:
            max_depth += file.count('*')
            max_depth += file.count('/')
            aql_query_dict['path'] = {"$match": file}
            # replace null string to *
        else:
            aql_query_dict['path'] = {"$match": file + "/*"}

    logging.debug("AQL query: items.find({})".format(aql_query_dict))
    artifacts = aql.aql('items.find', aql_query_dict)
    logging.debug('Artifacts count: {}'.format(len(artifacts)))
    artifacts_size = sum([x['size'] for x in artifacts])
    logging.debug('Summary size: {}'.format(size(artifacts_size)))

    print_str = out_as_du(artifacts, max_depth, human_readable, all)
    print(print_str)


APP_DESCRIPTION = "Summarize disk usage in JFrog Artifactory of the set of FILEs, recursively for directories."


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, description=APP_DESCRIPTION)

    # replace argparse.help, because du use -h flag for --human-readable
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit.')
    # Artifactory specific arguments
    parser.add_argument("--artifactory-url", action="store", required=True,
                        help="URL to artifactory, e.g: https://arti.example.com/artifactory", )
    parser.add_argument("--username", action="store", required=True,
                        help="user how have READ access to repository", )
    parser.add_argument("--password", action="store", required=True,
                        help="users password how have READ access to repository", )
    parser.add_argument("--repository", action="store", required=True,
                        help="Specify repository", )
    parser.add_argument("--verbose", "-v", "--debug", help="increase output verbosity", action="store_true")

    # du arguments
    parser.add_argument("--human-readable", "-h", action="store_true", required=False,
                        help="print sizes in human readable format (e.g., 1K 234M 2G)")
    parser.add_argument("--max-depth", action="store", required=False, default=100, type=int,
                        help="print the total for a directory (or file, with --all) only if it is N or fewer levels"
                             "below the command line argument;  --max-depth=0 is the same  as --summarize")
    parser.add_argument("--all", action="store_true",
                        help="write counts for all files, not just directories")
    parser.add_argument("--summarize", "-s", action="store_true",
                        help="display only a total for each argument")

    parser.add_argument("file", type=str, )

    args_ = parser.parse_args()
    return args_


def main():
    args = parse_args()
    if args.all and args.summarize:
        print('artifactory-du: cannot both summarize and show all entries', file=sys.stderr)

    args = args.__dict__
    if args.pop('summarize'):
        if args['max_depth'] != 100:
            print('artifactory-du: warning: summarizing is the same as using --max-depth=0', file=sys.stderr)
        args['max_depth'] = 0

    if args.pop('verbose'):
        init_logging()

    du(**args)


if __name__ == "__main__":
    main()
