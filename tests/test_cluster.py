from cluster import Cluster


def test_cluster():
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

    assert cluster.cluster['diff']['1']['2']['logic'] == 'unknown'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unknown'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unknown'

    cluster.set_manual('1', '2', 'equiv')

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unknown'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unknown'

    cluster.set_manual('2', '3', 'equiv')

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'equiv'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'equiv'

    cluster.set_manual('2', '3', 'unequiv')

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unequiv'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unequiv'

    cluster.set_manual('2', '3', 'unknown')

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unknown'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unknown'

    cluster.set_manual('3', '4', 'equiv')

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unknown'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unknown'

    assert cluster.cluster['diff']['3']['4']['logic'] == 'equiv'

    cluster.set_auto('2', '3', 'unequiv')
    cluster.update_diff()

    assert cluster.cluster['diff']['1']['2']['logic'] == 'equiv'

    assert cluster.cluster['diff']['2']['3']['logic'] == 'unequiv'

    assert cluster.cluster['diff']['1']['3']['logic'] == 'unequiv'

    assert cluster.cluster['diff']['3']['4']['logic'] == 'equiv'

