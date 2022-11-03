from input import Input
from output import Output
from paracomp import Paracomp

def main(path: str):
    # 读取输入, from_clusters 表示会读取保存的 clusters
    print('读取输入中...')
    input = Input(path, from_clusters=True)
    # 进行并行比较
    print('执行比较中...')
    paracomp = Paracomp(path, input)
    for cluster_name in paracomp.get_cluster_names():
        # 如果是加载的则跳过
        if input.clusters[cluster_name].cluster['is_loaded']:
            continue
        paracomp.run(cluster_name)
    # 对结果进行保存
    output = Output(path, input.clusters)
    print('保存 csv 文件中...')
    output.save_diff_list_to_csv()
    # 同时也保存 clusters 到 clusters 文件夹
    print('保存 clusters 文件中...')
    output.save_clusters()
    print('完成!')

if __name__ == "__main__":
    main("./data")