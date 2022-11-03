if __name__ == '__main__':
    import sys
    sys.path.append("..")
import json
import os
from cluster import Cluster
from typing import Dict


class Input:

    def __init__(self, path) -> None:
        '''
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
        # 判断是否存在中间文件夹 path/clusters, 有则加载
        clusters_path = os.path.join(path, "clusters")
        if os.path.exists(clusters_path) and os.path.isdir(clusters_path):
            self.clusters = self.load_clusters(path)
        else:
            self.clusters = Input.create_clusters_from_path(path)

    def load_clusters(self, path) -> Dict[str, Cluster]:
        clusters_path = os.path.join(path, "clusters")
        clusters: Dict[str, Cluster] = {}
        for cluster_name in os.listdir(clusters_path):
            cluster_path = os.path.join(clusters_path, cluster_name)
            if os.path.isdir(cluster_path):
                for file_name in os.listdir(cluster_path):
                    if file_name.endswith(".json"):
                        file_path = os.path.join(cluster_path, file_name)
                        cluster = json.loads(open(file_path, "r").read())
                        clusters[cluster_name] = Cluster(path, cluster)
        return clusters

    @staticmethod
    def create_empty_cluster() -> dict:
        '''
        初始化空 cluster
        '''
        return {
            "cluster_name": '',
            "random_input_generator": {
                "type": "empty"
            },
            "custom_input": [],
            "config": {
                "random_test_times": 10,
                "random_seed": 0,
            },
            "files": {},
            "equiv": [],
            "unequiv": [],
            "diff": {}
        }

    @staticmethod
    def create_cluster_from_path(path: str, cluster_name: str) -> Cluster:
        '''
        从 path 创建 cluster
        '''
        # 绝对路径
        input_path = os.path.abspath(os.path.join(path, 'input'))
        cluster_path = os.path.join(input_path, cluster_name)
        cluster = Input.create_empty_cluster()
        cluster['cluster_name'] = cluster_name
        # 读取 cluster_path 下的每个文件
        for file_name in os.listdir(cluster_path):
            file_path = os.path.join(cluster_path, file_name)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 各种配置文件
                        if file_name == 'stdin_format.txt':
                            cluster['random_input_generator']['type'] = 'stdin_format.txt'
                            cluster['random_input_generator']['content'] = content
                        elif file_name == 'stdin_format.py':
                            cluster['random_input_generator']['type'] = 'stdin_format.py'
                        elif file_name == 'config.json':
                            cluster['config'].update(json.loads(content))
                        else:
                            # 普通文件
                            cluster['files'][file_name] = {
                                'content': content,
                                'equiv_class': file_name
                            }
                except UnicodeDecodeError:
                    pass
            elif os.path.isdir(file_path):
                if file_name == 'custom_input':
                    # 自定义输入
                    for custom_input_file_name in os.listdir(file_path):
                        custom_input_file_path = os.path.join(
                            file_path, custom_input_file_name)
                        with open(custom_input_file_path, 'r', encoding='utf-8') as f:
                            cluster['custom_input'].append(f.read())
        _cluster = Cluster(path, cluster)
        _cluster.clear()
        return _cluster

    @staticmethod
    def create_clusters_from_path(path: str) -> Dict[str, Cluster]:
        '''
        从 path 创建 cluster
        '''
        clusters: Dict[str, Cluster] = {}
        # 绝对路径
        input_path = os.path.abspath(os.path.join(path, 'input'))
        for cluster_name in os.listdir(input_path):
            cluster_path = os.path.join(input_path, cluster_name)
            if os.path.isdir(cluster_path):
                clusters[cluster_name] = Input.create_cluster_from_path(
                    path, cluster_name)
        return clusters


def unit_test():
    input = Input('../data')
    print(input.clusters)


if __name__ == '__main__':
    unit_test()