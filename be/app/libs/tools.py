import os
import json
import zipfile

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


def unzip_file(zip_src, dst_dir):
    """
    解压zip文件
    :param zip_src: zip文件的全路径
    :param dst_dir: 要解压到的目的文件夹
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        return "请上传zip类型压缩文件"

