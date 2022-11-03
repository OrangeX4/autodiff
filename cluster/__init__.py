from typing import List


class Cluster:

    def __init__(self, path: str, cluster: dict):
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
        self.cluster = cluster
        # 过滤 unequiv
        self.filter_unequiv()

    def find(self, file: str) -> str:
        '''
        并查集的查找, 对 cluster 里的 files 的 equiv_class 进行查找
        '''
        # 查找
        node = file
        parent = self.cluster['files'][node]['equiv_class']
        while parent != node:
            node = parent
            parent = self.cluster['files'][node]['equiv_class']
        root = node

        # 路径压缩
        node = file
        while node != root:
            parent = self.cluster['files'][node]['equiv_class']
            self.cluster['files'][node]['equiv_class'] = root
            node = parent
        return root

    def union(self, file1: str, file2: str):
        '''
        并查集的合并, 对 cluster 里的 files 的 equiv_class 进行合并
        '''
        root1 = self.find(file1)
        root2 = self.find(file2)
        if root1 != root2:
            self.cluster['files'][root2]['equiv_class'] = root1

    def is_equiv(self, file1: str, file2: str) -> bool:
        '''
        判断两个文件是否等价
        '''
        return self.find(file1) == self.find(file2)

    def clear_equiv_class(self):
        '''
        清空 files 中的 equiv_class
        '''
        for file in self.cluster['files']:
            self.cluster['files'][file]['equiv_class'] = file

    def undo_equiv(self, file1: str, file2: str):
        '''
        从 equiv 中删除 [file1, file2], 并重新计算 equiv
        '''
        try:
            self.cluster['equiv'].remove([file1, file2])
        except:
            pass
        try:
            self.cluster['equiv'].remove([file2, file1])
        except:
            pass
        self.clear_equiv_class()
        for file1, file2 in self.cluster['equiv']:
            self.union(file1, file2)

    def filter_unequiv(self):
        '''
        过滤 unequiv 
        '''
        new_unequiv = set()
        for file1, file2 in self.cluster['unequiv']:
            new_unequiv.add((self.find(file1), self.find(file2)))
        self.cluster['unequiv'] = list(new_unequiv)

    def undo_unequiv(self, file1: str, file2: str):
        '''
        从 unequiv 中删除 [file1, file2]
        '''
        try:
            self.cluster['unequiv'].remove((file1, file2))
        except:
            pass
        try:
            self.cluster['unequiv'].remove((file2, file1))
        except:
            pass
        root1 = self.find(file1)
        root2 = self.find(file2)
        try:
            self.cluster['unequiv'].remove((root1, root2))
        except:
            pass
        try:
            self.cluster['unequiv'].remove((root2, root1))
        except:
            pass

    def clear(self):
        '''
        清空 cluster
        '''
        self.clear_equiv_class()
        self.cluster['equiv'] = []
        self.cluster['unequiv'] = []
        for file1 in self.cluster['files']:
            for file2 in self.cluster['files']:
                if file1 == file2:
                    continue
                if file1 not in self.cluster['diff']:
                    self.cluster['diff'][file1] = {}
                if file2 not in self.cluster['diff'][file1]:
                    self.cluster['diff'][file1][file2] = {
                        "auto": "unknown",
                        "manual": "unknown",
                        "logic": "unknown"
                    }
                self.cluster['diff'][file1][file2]['auto'] = 'unknown'
                self.cluster['diff'][file1][file2]['manual'] = 'unknown'
                self.cluster['diff'][file1][file2]['logic'] = 'unknown'

    def update_diff(self):
        '''
        更新 diff
        '''
        self.filter_unequiv()
        for file1 in self.cluster['files']:
            for file2 in self.cluster['files']:
                if file1 == file2:
                    continue
                if self.is_equiv(file1, file2):
                    self.cluster['diff'][file1][file2]['logic'] = 'equiv'
                else:
                    root1 = self.find(file1)
                    root2 = self.find(file2)
                    if (root1, root2) in self.cluster['unequiv'] or (root2, root1) in self.cluster['unequiv']:
                        self.cluster['diff'][file1][file2]['logic'] = 'unequiv'
                    else:
                        self.cluster['diff'][file1][file2]['logic'] = 'unknown'

    def set_manual(self, file1: str, file2: str, manual: str):
        '''
        设置 diff 中的 manual
        '''
        old_manual = self.cluster['diff'][file1][file2]['manual']
        self.cluster['diff'][file1][file2]['manual'] = manual
        self.cluster['diff'][file2][file1]['manual'] = manual
        if manual == 'equiv':
            if old_manual == 'unequiv':
                self.undo_unequiv(file1, file2)
            self.cluster['equiv'].append([file1, file2])
            self.union(file1, file2)
        elif manual == 'unequiv':
            if old_manual == 'equiv':
                self.undo_equiv(file1, file2)
            self.cluster['unequiv'].append((file1, file2))
        elif manual == 'unknown':
            if old_manual == 'equiv':
                self.undo_equiv(file1, file2)
            elif old_manual == 'unequiv':
                self.undo_unequiv(file1, file2)
        else:
            raise Exception('manual must be equiv, unequiv or unknown')
        self.update_diff()

    def set_auto(self, file1: str, file2: str, auto: str):
        '''
        设置 diff 中的 auto
        '''
        self.cluster['diff'][file1][file2]['auto'] = auto
        self.cluster['diff'][file2][file1]['auto'] = auto
        if auto == 'unequiv':
            self.cluster['unequiv'].append((file1, file2))


def unit_test():
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
            "1": {
                "content": "int main() { return 0; }",
                "equiv_class": "1"
            },
            "2": {
                "content": "int main() { return 0; }",
                "equiv_class": "2"
            },
            "3": {
                "content": "int main() { return 0; }",
                "equiv_class": "3"
            },
            "4": {
                "content": "int main() { return 0; }",
                "equiv_class": "4"
            }
        },
        "equiv": [],
        "unequiv": [],
        "diff": {}
    }
    cluster = Cluster('test', cluster)
    cluster.clear()
    cluster.set_manual('1', '2', 'equiv')
    cluster.set_manual('2', '3', 'equiv')
    cluster.set_manual('2', '3', 'unequiv')
    cluster.set_manual('2', '3', 'unknown')
    cluster.set_manual('3', '4', 'equiv')
    cluster.set_auto('2', '3', 'unequiv')
    cluster.update_diff()
    print(cluster.cluster)


if __name__ == '__main__':
    unit_test()
