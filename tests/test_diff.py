from diff import Diff


def test_diff_1():
    diff = Diff()

    file1 = './data/input/4A/48762087.cpp'
    file2 = './data/input/4A/84822638.cpp'

    _input = '2'

    diff.build(file1)
    diff.build(file2)

    output = {}
    result = diff.diff(file1, file2, _input, output)

    assert output[file1] == 'HELLO'

    assert output[file1] != output[file2]

    assert result is False


def test_diff_2():
    diff = Diff()

    file1 = './data/input/50A/21508887.cpp'
    file2 = './data/input/50A/21508898.cpp'

    _input = '4 5'

    diff.build(file1)
    diff.build(file2)

    output = {}
    result = diff.diff(file1, file2, _input, output)

    assert output[file1] == '10'

    assert output[file1] == output[file2]

    assert result is True