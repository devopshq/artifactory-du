from artifactory_du.du import out_as_du


def test_out_as_du_simple_human():
    artifacts = [
        {'name': 'filename1.txt',
         'path': 'level1',
         'size': 1024,
         },
    ]
    expected_result = """1K    level1"""
    result = out_as_du(artifacts, max_depth=1, human_readable=True, all=False)
    assert expected_result == result


def test_out_as_du_simple_byte():
    artifacts = [
        {'name': 'filename1.txt',
         'path': 'level1',
         'size': 1024,
         },
    ]
    expected_result = """1024    level1"""
    result = out_as_du(artifacts, max_depth=1, human_readable=False, all=False)
    assert expected_result == result


ARTIFACTS = [
    {'name': 'filename11.txt',
     'path': '1/2',
     'size': 1024,
     },
    {'name': 'filename12.txt',
     'path': '1/2',
     'size': 1024,
     },
    {'name': 'filename21.txt',
     'path': '2/2',
     'size': 1024,
     },
    {'name': 'filename22.txt',
     'path': '2/2',
     'size': 1024,
     },
]


def test_out_as_du_max_depth_1():
    expected_result = """2K    1
2K    2"""
    result = out_as_du(ARTIFACTS, max_depth=1, human_readable=True, all=False)
    assert expected_result == result


def test_out_as_du_max_depth_2():
    expected_result = """2K    1/2
2K    2/2"""
    result = out_as_du(ARTIFACTS, max_depth=2, human_readable=True, all=False)
    assert expected_result == result


def test_out_as_du_max_depth_all():
    expected_result = """1K    1/2/filename11.txt
1K    1/2/filename12.txt
1K    2/2/filename21.txt
1K    2/2/filename22.txt"""
    result = out_as_du(ARTIFACTS, max_depth=100, human_readable=True, all=True)
    assert expected_result == result
