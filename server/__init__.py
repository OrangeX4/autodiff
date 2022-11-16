if __name__ == '__main__':
    import sys
    sys.path.append("..")
from flask import Flask, request
import webbrowser
from typing import Dict
from input import Input
from output import Output
from paracomp import Paracomp
from cluster import Cluster

# Flask
app = Flask(__name__,
            static_url_path='',
            static_folder='static')
# data 路径
path = "../data"

# 加载
print('读取输入中...')
input = Input(path, from_clusters=True)
# Clusters
clusters: Dict[str, Cluster] = input.clusters
# 输出模块
output = Output(path, clusters)

# 打开网页 http://localhost:7376/
if __name__ == '__main__':
    webbrowser.open('http://localhost:7376/')


def get_cluster(cluster_name) -> Dict:
    '''
    获取 cluster dict 的函数, 并且更新 diff_list
    '''
    cluster = clusters[cluster_name]
    cluster_dict = cluster.cluster
    cluster_dict['diff_list'] = output.cluster_to_diff_list(cluster_name)
    return cluster_dict


# 进行并行比较
print('加载比较器...')
paracomp = Paracomp(path, input)
# for cluster_name in paracomp.get_cluster_names():
#     # 如果是加载的则跳过
#     if input.clusters[cluster_name].cluster['is_loaded']:
#         continue
#     paracomp.run(cluster_name)


@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route("/")
def handle_root():
    return app.send_static_file('index.html')


@app.route("/clusters", methods=['GET'])
def handle_clusters():
    result = {}
    for cluster_name in clusters:
        result[cluster_name] = get_cluster(cluster_name)
    return result


@app.route("/csv", methods=['GET'])
def handle_csv():
    return output.diff_list_to_csv("logic")


@app.route("/cluster/<cluster_name>", methods=['GET'])
def handle_cluster(cluster_name):
    if cluster_name in clusters:
        return get_cluster(cluster_name)
    else:
        return {
            'status': 'error',
            'message': 'No such cluster.'
        }


@app.route("/run", methods=['POST'])
def handle_run():
    '''
    { "cluster_name": cluster_name }
    '''
    data = request.json
    if data is not None and 'cluster_name' in data:
        if data['cluster_name'] in clusters:
            paracomp.run(data['cluster_name'])
            # 保存结果
            output.save_clusters()
            return get_cluster(data['cluster_name'])
        else:
            return {
                'status': 'error',
                'message': 'No such cluster.'
            }
    else:
        return {
            'status': 'error',
            'message': 'There is no "cluster_name" in request.'
        }


@app.route("/update", methods=['POST'])
def handle_update():
    '''
    {
        "cluster_name": cluster_name,
        "file1": file1,
        "file2": file2,
        "manual": manual,
    }
    '''
    data = request.json
    if data is not None:
        if 'cluster_name' in data \
                and 'file1' in data \
                and 'file2' in data \
                and 'manual' in data:
            if data['cluster_name'] in clusters:
                cluster = clusters[data['cluster_name']]
                cluster.set_manual(
                    data['file1'], data['file2'], data['manual'])
                # 保存结果
                output.save_clusters()
                return get_cluster(data['cluster_name'])
            else:
                return {
                    'status': 'error',
                    'message': 'No such cluster.'
                }
        else:
            return {
                'status': 'error',
                'message': 'There is no neccessary key in request.'
            }
    else:
        return {
            'status': 'error',
            'message': 'Data is empty.'
        }


if __name__ == '__main__':
    app.run(debug=False, port=7376, host='0.0.0.0')
