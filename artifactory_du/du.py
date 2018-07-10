from itertools import groupby

from hurry.filesize import size


def out_as_du(artifacts, max_depth, human_readable=False, all=False):
    """
    Return result as original linux cli utility du
    Method have some magic, I did not write comment and forget how it works :(
    But we have test, so you can refactor this :)
    :param artifacts: List of dict with two key (mandatory): path, name, size (in byte)
    :param max_depth:
    :param human_readable:
    :param all:
    :return:
    """
    # Add full path with path and name
    for artifact in artifacts:
        artifact['fullpath'] = artifact['path'] + '/' + artifact['name']
    path_key = 'fullpath' if all else 'path'

    artifacts = sorted(artifacts, key=lambda x: x[path_key])
    depth = lambda path_, max_depth_: tuple(path_.split('/', maxsplit=max_depth_)[:max_depth_])
    artifacts_group = groupby(
        artifacts,
        key=lambda x: depth(x[path_key], max_depth)
    )

    result = []
    for group, artifacts_ in artifacts_group:
        artifacts_size = sum([x['size'] for x in artifacts_])
        if human_readable:
            artifacts_size = size(artifacts_size)
        artifacts_size = str(artifacts_size)
        result.append("{}{}".format(artifacts_size.ljust(8), '/'.join(group if group else '/')))
    return "\n".join(result)
