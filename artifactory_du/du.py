from itertools import groupby

from hurry.filesize import size


def out_as_du(artifacts, max_depth, human_readable=False, all=False, summarize=False):
    """
    Return result as original linux cli utility du
    :param artifacts: List of dict with two key (mandatory): path, name, size (in byte)
    :param max_depth:
    :param human_readable:
    :return:
    """
    artifacts = sorted(artifacts, key=lambda x: x['path'])
    depth = lambda path_, max_depth_: tuple(path_.split('/', maxsplit=max_depth_)[:max_depth_])
    artifacts_group = groupby(
        artifacts,
        key=lambda x: depth(x['path'], max_depth)
    )

    result = []
    for group, artifacts_ in artifacts_group:
        artifacts_size = sum([x['size'] for x in artifacts_])
        if human_readable:
            artifacts_size = size(artifacts_size)
        result.append("{}    {}".format(artifacts_size, '/'.join(group)))
    return "\n".join(result)
