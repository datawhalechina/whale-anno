import os
import json


def make_dir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)


# 将json数据写入.json文件
def write_json(json_file_path, data):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=lambda o: o.__dict__)


# 加载json文件中的json数据
def read_json_file(json_file_name):
    with open(json_file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# 读取txt文件
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data
