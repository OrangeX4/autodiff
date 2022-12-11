from input import Input
from output import Output
from paracomp import Paracomp


def test_integration():
    path = './data'
    # 读取输入, from_clusters 表示会读取保存的 clusters
    input = Input(path, from_clusters=True)
    # 进行并行比较
    paracomp = Paracomp(path, input)
    for cluster_name in paracomp.get_cluster_names():
        # 如果是加载的则跳过
        if input.clusters[cluster_name].cluster['is_loaded']:
            continue
        paracomp.run(cluster_name)
    # 对结果进行保存
    output = Output(path, input.clusters)

    # 确认比对结果
    assert output.clusters['4A'].cluster['diff']['101036360.cpp']['117364748.cpp']['auto'] == 'unequiv'
    
    assert output.clusters['4A'].cluster['diff']['101036360.cpp']['117364748.cpp']['logic'] == 'unequiv'

    assert output.clusters['4A'].cluster['diff']['173077807.cpp']['84822639.cpp']['auto'] == 'equiv'

    assert output.clusters['4A'].cluster['diff']['173077807.cpp']['84822639.cpp']['logic'] == 'unknown'

    assert output.clusters['50A'].cluster['diff']['138805414.cpp']['21508898.cpp']['auto'] == 'unequiv'

    assert output.clusters['50A'].cluster['diff']['138805414.cpp']['21508898.cpp']['logic'] == 'unequiv'
    
    assert output.clusters['50A'].cluster['diff']['138805414.cpp']['142890373.cpp']['auto'] == 'equiv'

    assert output.clusters['50A'].cluster['diff']['138805414.cpp']['142890373.cpp']['logic'] == 'unknown'

    assert output.clusters['50A'].cluster['diff']['142890373.cpp']['138805414.cpp']['auto'] == 'equiv'
    
    assert output.clusters['50A'].cluster['diff']['142890373.cpp']['138805414.cpp']['logic'] == 'unknown'

