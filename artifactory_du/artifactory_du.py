import argparse
import logging
import sys
from datetime import date, timedelta

import requests
from artifactory import ArtifactoryPath
from hurry.filesize import size
from requests_kerberos import HTTPKerberosAuth, DISABLED

from artifactory_du.du import out_as_du
from artifactory_du.version import __version__

requests.packages.urllib3.disable_warnings()


def init_logging():
    """
    Init logging
    :return:
    """
    logger_format_string = "%(levelname)-8s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=logger_format_string, stream=sys.stdout)


def artifactory_aql(
    artifactory_url="",
    access_token="",
    username="",
    password="",
    aql_query_dict=None,
    kerberos=False,
    verify=False,
    artifactory_path=None,
):
    """
    Send AQL to Artifactory and get list of Artifacts
    :param artifactory_path: (ArtifactoryPath) if provided then use this object as URL, username and password
    :param artifactory_url: URL path to artifactory (not the repo), not applied with artifactory_path
    :param access_token: access token for authentication, not applied with artifactory_path
    :param username: username for authentication, not applied with artifactory_path
    :param password: password for authentication, not applied with artifactory_path
    :param kerberos: Boolean if kerberos authentication should be used
    :param verify: Boolean if SSL certificate should be checked
    :param aql_query_dict: (dict) that you get from prepare_aql function
    :return:
    """
    if artifactory_path:
        aql = artifactory_path
    elif access_token:
        aql = ArtifactoryPath(artifactory_url, token=access_token, verify=verify)
    else:
        if kerberos:
            auth = HTTPKerberosAuth(mutual_authentication=DISABLED, sanitize_mutual_error_response=False)
        else:
            if not password:
                raise ValueError("argument 'password' needs to be set for basic authentication")
            auth = (username, password)
        aql = ArtifactoryPath(artifactory_url, auth=auth, verify=verify)

    logging.debug("AQL query: items.find({})".format(aql_query_dict))
    artifacts = aql.aql("items.find", aql_query_dict)
    logging.debug("Artifacts count: {}".format(len(artifacts)))
    artifacts_size = sum([x["size"] for x in artifacts])
    logging.debug("Summary size: {}".format(size(artifacts_size)))

    return artifacts


def prepare_aql(file, max_depth, repository, without_downloads, older_than):
    """
    Prepare AQL and calculate new max_depth for du
    :param older_than:
    :param file: pattern for file
    :param max_depth:
    :param repository:
    :return: tuple - aql.dict and new max_depth
    """
    aql_query_dict = {"repo": repository}
    if file:
        # Remove first / in path: /path => path
        file = file[1:] if file.startswith("/") else file
        if "*" in file:
            max_depth += file.count("*")
            max_depth += file.count("/")
            aql_query_dict["path"] = {"$match": file}
            # replace null string to *
        else:
            aql_query_dict["path"] = {"$match": file + "/*"}

    if without_downloads:
        aql_query_dict["stat.downloads"] = {"$eq": None}
        logging.debug("Counts for artifacts without downloads")

    if older_than:
        today = date.today()
        older_than_date = today - timedelta(older_than)
        older_than_date_txt = older_than_date.isoformat()
        aql_query_dict["created"] = {"$lt": older_than_date_txt}
        logging.debug("Counts for artifacts older than {}".format(older_than_date_txt))

    return aql_query_dict, max_depth


APP_DESCRIPTION = "Summarize disk usage in JFrog Artifactory of the set of FILEs, recursively for directories."


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, description=APP_DESCRIPTION)

    # replace argparse.help, because du use -h flag for --human-readable
    parser.add_argument("--help", action="help", default=argparse.SUPPRESS, help="show this help message and exit.")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))

    # Artifactory CONNECTION arguments
    parser.add_argument(
        "--artifactory-url",
        action="store",
        required=True,
        help="URL to artifactory, e.g: https://arti.example.com/artifactory",
    )
    parser.add_argument(
        "--repository",
        action="store",
        required=True,
        help="Specify repository",
    )
    parser.add_argument("--ignorecert", help="ignore SSL certificate of the artifactory server", action="store_true")
    parser.add_argument("--verbose", "-v", "--debug", help="increase output verbosity", action="store_true")

    # Authentication arguments
    auth_args = parser.add_mutually_exclusive_group(required=True)
    auth_args.add_argument(
        "--username",
        action="store",
        help="user how have READ access to repository (password needed in this case)",
    )
    auth_args.add_argument(
        "--kerberos",
        "-k",
        action="store_true",
        help="use kerberos authentication (no password needed here)",
    )
    auth_args.add_argument(
        "--access-token",
        action="store",
        help="access token how have READ access to repository (no password needed here)"
    )

    parser.add_argument(
        "--password",
        action="store",
        help="users password how have READ access to repository",
    )

    # Artifactory SPECIFIC arguments
    parser.add_argument("--without-downloads", action="store_true", help="Find items that have never been downloaded")
    parser.add_argument(
        "--older-than", action="store", default=0, type=int, help="only counts size for files older than"
    )

    # du arguments
    parser.add_argument(
        "--human-readable",
        "-h",
        action="store_true",
        required=False,
        help="print sizes in human readable format (e.g., 1K 234M 2G)",
    )
    parser.add_argument(
        "--max-depth",
        action="store",
        required=False,
        default=100,
        type=int,
        help="print the total size for a directory (or file, with --all) only if it is N or fewer levels"
        "below the command line argument;  --max-depth=0 is the same  as --summarize",
    )
    parser.add_argument("--all", action="store_true", help="write counts for all files, not just directories")
    parser.add_argument("--summarize", "-s", action="store_true", help="display only a total for each argument")

    parser.add_argument(
        "file",
        type=str,
    )

    args_ = parser.parse_args()
    return args_


def main():
    args = parse_args()
    if args.all and args.summarize:
        print("artifactory-du: cannot both summarize and show all entries", file=sys.stderr)

    if args.summarize:
        if args.max_depth != 100:
            print("artifactory-du: warning: summarizing is the same as using --max-depth=0", file=sys.stderr)
        args.max_depth = 0

    if args.verbose:
        init_logging()

    aql_query_dict, max_depth_print = prepare_aql(
        file=args.file,
        max_depth=args.max_depth,
        repository=args.repository,
        without_downloads=args.without_downloads,
        older_than=args.older_than,
    )
    artifacts = artifactory_aql(
        artifactory_url=args.artifactory_url,
        access_token=args.access_token,
        username=args.username,
        password=args.password,
        aql_query_dict=aql_query_dict,
        kerberos=args.kerberos,
        verify=not args.ignorecert,
    )
    print_str = out_as_du(artifacts, max_depth_print, args.human_readable, args.all)
    print(print_str)


if __name__ == "__main__":
    main()
