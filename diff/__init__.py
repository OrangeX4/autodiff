import platform
from subprocess import PIPE, Popen
from os import path


def format_string_with_file(string: str, file: str):
    '''
    对 string 进行格式化, 用 file 中的内容 (会被转为绝对路径) 替换 string 中的
    - {file}
    - {fileBasenameNoExtension}
    - {fileBasename}
    - {fileDirname}
    - {fileExtname}
    - {cwd}
    '''
    # get absolute path
    file = path.abspath(file)
    file_map = {
        'file': file,
        'fileNoExtension': path.splitext(file)[0],
        'fileBasenameNoExtension': path.splitext(path.basename(file))[0],
        'fileBasename': path.basename(file),
        'fileDirname': path.dirname(file),
        'fileExtname': path.splitext(file)[1],
        'cwd': path.abspath(path.curdir)
    }
    return string.format(**file_map)


class Executor:

    def __init__(self, execute_cmd: str, build_cmd=None, clean_cmd=None) -> None:
        '''
        execute_cmd: 用于执行可执行程序的命令
        build_cmd: 用于构建可执行程序的命令
        clean_cmd: 用于清理可执行程序的命令
        '''
        self.execute_cmd = execute_cmd
        self.build_cmd = build_cmd
        self.clean_cmd = clean_cmd

    def _exec(self, file: str, cmd) -> None:
        if cmd is None:
            return
        cmd = format_string_with_file(cmd, file)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        process.communicate()

    def build(self, file: str) -> None:
        self._exec(file, self.build_cmd)

    def clean(self, file: str) -> None:
        self._exec(file, self.clean_cmd)

    def execute(self, file: str, _input: str) -> str:
        cmd = format_string_with_file(self.execute_cmd, file)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output, err = process.communicate(input=_input.encode())
        if err:
            # raise Exception(err.decode())
            return err.decode()
        return output.decode()


class Diff:

    '''
    Diff 模块, 用于比较两个文件执行的差异
    '''

    def __init__(self) -> None:
        # 获取当前操作系统类型, Windows 或 Linux
        self.os = platform.system()
        # 注册执行器
        self.executor_map = {
            'c': {
                'Windows': Executor('{fileNoExtension}.exe',
                    'gcc {file} -o "{fileNoExtension}.exe"',
                    'del "{fileNoExtension}.exe"'),
                'Linux': Executor('./{fileNoExtension}.out',
                    'gcc {file} -o "{fileNoExtension}.out"',
                    'rm "{fileNoExtension}.out"')
            },
            'cpp': {
                'Windows': Executor('{fileNoExtension}.exe',
                    'g++ "{file}" -o "{fileNoExtension}.exe"',
                    'del "{fileNoExtension}.exe"'),
                'Linux': Executor('{fileNoExtension}.out',
                    'g++ "{file}" -o "{fileNoExtension}.out"',
                    'rm "{fileNoExtension}.out"')
            },
            'py': {
                'Windows': Executor('python "{file}"'),
                'Linux': Executor('python3 "{file}"')
            },
        }

    def build(self, file: str) -> None:
        '''
        为文件生成可执行文件
        '''
        # 获取文件后缀
        suffix = path.splitext(file)[1][1:]
        # 获取执行器
        executor = self.executor_map.get(suffix, {}).get(self.os)
        if executor is None:
            raise Exception('不支持的文件类型')
        executor.build(file)

    def clean(self, file: str) -> None:
        '''
        清理文件
        '''
        # 获取文件后缀
        suffix = path.splitext(file)[1][1:]
        # 获取执行器
        executor = self.executor_map.get(suffix, {}).get(self.os)
        if executor is None:
            raise Exception('不支持的文件类型')
        executor.clean(file)

    def diff(self, file1: str, file2: str, _input: str, saved_output=None) -> bool:
        '''
        对两个文件使用同一个输出 (需要事先生成可执行文件), 判断它们的输出是否相等
        返回 True 表示相等, False 表示不相等
        '''
        # 获取执行器
        executor1 = self.executor_map.get(
            path.splitext(file1)[1][1:], {}).get(self.os)
        executor2 = self.executor_map.get(
            path.splitext(file2)[1][1:], {}).get(self.os)
        if executor1 is None or executor2 is None:
            raise Exception('不支持的文件类型')
        # 执行文件
        output1 = executor1.execute(file1, _input)
        output2 = executor2.execute(file2, _input)
        # 保存输出
        if saved_output is not None and isinstance(saved_output, dict):
            saved_output[file1] = output1
            saved_output[file2] = output2
        # 比较输出
        return output1 == output2


def unit_test():
    diff = Diff()
    file1 = '../data/input/4A/48762087.cpp'
    file2 = '../data/input/4A/84822638.cpp'
    _input = '2'
    diff.build(file1)
    diff.build(file2)
    output = {}
    result = diff.diff(file1, file2, _input, output)
    print('input:', _input)
    print('output:', output)
    print('result:', result)


if __name__ == '__main__':
    unit_test()
