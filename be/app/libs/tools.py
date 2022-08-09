import os
import json
import zipfile
import tarfile
# import rarfile
# import py7zr

from os import rename
from os import listdir
from shutil import move
import base64

def get_cn_name(name):
    try:
        return name.encode('cp437').decode('GBK')
    except:
        return name

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

# 自适配读取文件
def read_file(file_path):
    ext = file_path.split('.')[-1]
    if ext in ['jpg', 'png']:
        return read_img_file(file_path)
    elif ext in ['txt']:
        return read_txt_file(file_path)
    return ''

# 读取img文件
def read_img_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode("ascii")

# 读取txt文件
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def get_project_file(project_path):

    file_name = os.listdir(project_path)
    file_name.remove('anno.json')
    file_name.remove('config.json')
    return file_name


def unzip_file(zip_src, dst_dir):
    """
    解压数据文件
    :param zip_src: 压缩包文件的全路径
    :param dst_dir: 要解压到的项目文件夹
    :return:
    """

    if zipfile.is_zipfile(zip_src):
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
            # Here to deal with chinese encode in module zipfile and rarfile
            os.replace(dst_dir + '/' + file, dst_dir + '/' + get_cn_name(file))
        return "unzip .zip file success"
    # elif rarfile.is_rarfile(zip_src):
    #     fr = rarfile.RarFile(zip_src, "r")
    #     print(fr.namelist())
    #     for file in fr.namelist():
    #         fr.extract(file, dst_dir)
    #     return "unzip .rar file success"
    # elif py7zr.is_7zfile(zip_src):
    #     f7z = py7zr.SevenZipFile(zip_src, "r")
    #     f7z.extractall(path=dst_dir)
    #     f7z.close()
    elif tarfile.is_tarfile(zip_src):

        ft = tarfile.TarFile(zip_src, "r")
        print(ft.getnames())
        for file in ft.getnames():
            ft.extract(file, dst_dir)

    else:
        return "请上传.zip .tar格式的文件"
