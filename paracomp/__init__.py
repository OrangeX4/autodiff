if __name__ == '__main__':
    import sys
    sys.path.append("..")
import multiprocessing
import random
import os
from input import Input
from generator import Generator
from diff import Diff


class Paracomp:

    def __init__(self, path: str, input: Input):
        '''
        并行计算模块, 使用多进程进行并行计算
        cluster = {
            "cluster_name": "4A",
            "random_input_generator": {
                "type": "stdin_format.txt",
                "content": "int(1, 3)"
            },
            "custom_input": [
                "1",
                "2"
            ],
            "config": {
                "random_test_times": 10,
                "random_seed": 0,
            },
            "files": {
                "48762087.cpp": {
                    "content": "int main() { return 0; }",
                    "equiv_class": "48762087.cpp"
                },
                "84822638.cpp": {
                    "content": "int main() { return 0; }",
                    "equiv_class": "48762087.cpp"
                }
            },
            "equiv": [["48762087.cpp", "84822638.cpp"]],
            "unequiv": [],
            "diff": {
                "48762087.cpp": {
                    "84822638.cpp": {
                        "auto": "unknown",
                        "manual": "equiv",
                        "logic": "equiv"
                    }
                },
                "84822638.cpp": {
                    "48762087.cpp": {
                        "auto": "unknown",
                        "manual": "equiv",
                        "logic": "equiv"
                    }
                }
            }
        }
        '''
        self.path = path
        self.input = input
        self.diff = Diff()
        self.proc_num = 8

    def get_cluster_names(self):
        return self.input.clusters.keys()

    def generate(self, cluster_name: str) -> str:
        '''
        生成随机测试用例
        '''
        cluster = self.input.clusters[cluster_name]
        cluster_dict = cluster.cluster
        if "random_input_generator" in cluster_dict:
            generator = cluster_dict["random_input_generator"]
            if "type" in generator:
                if generator["type"] == "stdin_format.txt":
                    return Generator.generate_from_txt(generator["content"])
                elif generator["type"] == "stdin_format.py":
                    return Generator.generate_from_py(generator["content"])
        return ''

    def diff_func(self, cluster_name: str, file1: str, file2: str) -> bool:
        cluster = self.input.clusters[cluster_name]
        cluster_dict = cluster.cluster
        # 如果完全相同, 则直接返回
        if cluster_dict['files'][file1]['content'] == cluster_dict['files'][file2]['content']:
            return True
        # 设定随机种子
        _file1 = os.path.abspath(os.path.join(
            self.path, 'input', cluster_name, file1))
        _file2 = os.path.abspath(os.path.join(
            self.path, 'input', cluster_name, file2))
        seed = int(cluster_dict['config']['random_seed'])
        if seed:
            random.seed(seed)
        # 随机测试
        for _ in range(int(cluster_dict['config']['random_test_times'])):
            if not self.diff.diff(_file1, _file2, self.generate(cluster_name)):
                return False
        custom_input = cluster_dict['custom_input']
        # 自定义测试
        for input in custom_input:
            if not self.diff.diff(_file1, _file2, input):
                return False
        return True

    def run(self, cluster_name: str):
        '''
        运行多进程并行计算
        '''
        cluster = self.input.clusters[cluster_name]
        cluster_dict = cluster.cluster
        result = {}

        # 生成所有可执行文件
        build_pool = multiprocessing.Pool(self.proc_num)
        for file in cluster_dict['files']:
            file_path = os.path.abspath(os.path.join(
                self.path, 'input', cluster_name, file))
            build_pool.apply_async(self.diff.build, args=(file_path,))
        build_pool.close()
        build_pool.join()

        # 对文件对进行比较
        diff_pool = multiprocessing.Pool(self.proc_num)
        for file1 in cluster_dict["files"]:
            result[file1] = {}
            for file2 in cluster_dict["files"]:
                # 判断字符串大小, 保证不重复
                if file1 >= file2:
                    continue
                # 为进程池加入任务
                result[file1][file2] = diff_pool.apply_async(
                    self.diff_func, args=(cluster_name, file1, file2))
        diff_pool.close()
        diff_pool.join()

        # 获取执行结果
        for file1 in result:
            for file2 in result[file1]:
                res = result[file1][file2].get()
                cluster.set_auto(file1, file2, 'equiv' if res else 'unequiv')
        cluster.update_diff()


def unit_test():
    paracomp = Paracomp('../data', Input('../data'))
    print(paracomp.get_cluster_names())
    paracomp.run('4A')
    print(paracomp.input.clusters['4A'].cluster)


if __name__ == '__main__':
    unit_test()
