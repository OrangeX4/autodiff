import json
import os
from typing import Dict
from cluster import Cluster


class Output:

    def __init__(self, path: str, clusters: Dict[str, Cluster]) -> None:
        self.path = path
        self.clusters = clusters

    def save_clusters(self) -> None:
        '''
        保存到 path/clusters 文件夹
        '''
        clusters_path = os.path.abspath(os.path.join(self.path, "clusters"))
        # 对 clusters 里的每个 cluster 保存一个 json
        for cluster_name in self.clusters:
            cluster = self.clusters[cluster_name]
            cluster_json_path = os.path.join(
                clusters_path, cluster_name + '.json')
            with open(cluster_json_path, 'w') as f:
                f.write(json.dumps(cluster.cluster, indent=4))

    def clusters_to_diff_list(self) -> list:
        '''
        将 clusters 转换为 diff_list, 其中 list 中每个元素为 (file1 < file2)
        {
            "cluster_name": cluster_name,
            "file1": file1,
            "file2": file2,
            "auto": auto,
            "manual": manual,
            "logic": logic
        }
        '''
        diff_list = []
        for cluster_name in self.clusters:
            diff_list += self.cluster_to_diff_list(cluster_name)
        return diff_list

    def cluster_to_diff_list(self, cluster_name: str) -> list:
        '''
        将 clusters 转换为 diff_list, 其中 list 中每个元素为 (file1 < file2)
        {
            "cluster_name": cluster_name,
            "file1": file1,
            "file2": file2,
            "auto": auto,
            "manual": manual,
            "logic": logic
        }
        '''
        diff_list = []
        cluster_dict = self.clusters[cluster_name].cluster
        for file1 in cluster_dict["files"]:
            for file2 in cluster_dict["files"]:
                if file1 < file2:
                    diff_list.append({
                        "cluster_name": cluster_name,
                        "file1": file1,
                        "file2": file2,
                        "auto": cluster_dict["diff"][file1][file2]["auto"],
                        "manual": cluster_dict["diff"][file1][file2]["manual"],
                        "logic": cluster_dict["diff"][file1][file2]["logic"]
                    })
        return diff_list


    def diff_list_to_csv(self, mode="auto") -> Dict:
        diff_list = self.clusters_to_diff_list()
        equal_csv_content = "file1,file2"
        unknown_csv_content = "file1,file2"
        inequal_csv_content = "file1,file2"
        for diff in diff_list:
            _file1 = f'input/{diff["cluster_name"]}/{diff["file1"]}'
            _file2 = f'input/{diff["cluster_name"]}/{diff["file2"]}'
            if diff[mode] == "equiv":
                equal_csv_content += f'\n{_file1},{_file2}'
            elif diff[mode] == "unknown":
                unknown_csv_content += f'\n{_file1},{_file2}'
            elif diff[mode] == "unequiv":
                inequal_csv_content += f'\n{_file1},{_file2}'
        return {
            "equal_csv_content": equal_csv_content,
            "unknown_csv_content": unknown_csv_content,
            "inequal_csv_content": inequal_csv_content
        }
        
    
    def save_diff_list_to_csv(self, mode="auto") -> None:
        '''
        保存到 path/output/equal.csv 和 path/output/inequal.csv
        格式为 input/cluster_name/file1,input/cluster_name/file2
        其中是否 equal 只取决于 auto == 'equiv' 与 auto == 'unequiv'
        '''
        equal_csv_path = os.path.abspath(
            os.path.join(self.path, "output", "equal.csv"))
        unknown_csv_path = os.path.abspath(
            os.path.join(self.path, "output", "unknown.csv"))
        inequal_csv_path = os.path.abspath(
            os.path.join(self.path, "output", "inequal.csv"))
        content_dict = self.diff_list_to_csv(mode)
        with open(equal_csv_path, 'w') as f:
            f.write(content_dict["equal_csv_content"])
        with open(unknown_csv_path, 'w') as f:
            f.write(content_dict["unknown_csv_content"])
        with open(inequal_csv_path, 'w') as f:
            f.write(content_dict["inequal_csv_content"])
