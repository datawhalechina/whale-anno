from ...config.setting import PROJECT_PATH, ANNO_OUTPUT_PATH, DOWNLOAD_FILE_LOCATION

from ...libs.redprint import RedPrint

from flask import request, send_file, Response, send_from_directory, make_response
import json
import os

from ...entities.entities import ReturnInfo, FileInfo
from ...libs.tools import read_json_file, read_txt_file, write_json, get_project_file
import threading
import time

#
api = RedPrint('files')


@api.route('/query', methods=['GET'])
def query_file():
    ret_info = ReturnInfo()
    try:
        project_name = request.args.get("projectName").strip()
        page_number = int(request.args.get("pageNumber"))
        page_size = int(request.args.get("pageSize"))

        project_path = PROJECT_PATH.format(project_name)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        file_names = os.listdir(project_path)
        if 'config.json' in file_names:
            file_names.remove('config.json')
        if 'anno.json' in file_names:
            file_names.remove('anno.json')

        for file_name in file_names[(page_number - 1) * page_size: (page_number - 1) * page_size + page_size]:
            anno_output_path = ANNO_OUTPUT_PATH.format(project_name, file_name)
            file_info = FileInfo()
            file_info.fileName = file_name
            file_info.isAnno = os.path.exists(anno_output_path)
            ret_info.info.append(file_info)

        ret_info.errCode = 0

        ret_info.total = len(file_names)

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(ret_info, default=lambda o: o.__dict__)


@api.route('/get_labels', methods=['GET'])
def get_lables():
    ret_info = ReturnInfo()
    try:

        download_json = []
        project_name = request.args.get("projectName")
        project_path = PROJECT_PATH.format(project_name)
        print(project_path)
        project_file_list = get_project_file(project_path)
        print(project_file_list)
        # current_filename = request.args.get("current_filename")
        anno_data_set = set()
        anno_data = read_json_file(PROJECT_PATH.format(project_name) + '/anno.json')
        for item in anno_data:
            item_dict = {'file': item['fileName'],
                         # 'text': read_txt_file(PROJECT_PATH.format(project_name) + '/' + item['fileName']),
                         'labels': list(set([x['type'] for x in item["annoDetails"]]))}
            print(item_dict)
            anno_data_set.add(item['fileName'])
            download_json.append(item_dict)
        #add no label data
        for filename in set(project_file_list).difference(anno_data_set):
            item_dict = {'file': filename,
                         'labels': []
                         }
            download_json.append(item_dict)

        # print(set(project_file_list).difference(anno_data_set))

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(download_json, default=lambda o: o.__dict__)

@api.route('/get_anno_json', methods=['GET'])
@api.route('/get_json', methods=['GET'])
def get_anno_json():
    project_name = request.args.get("projectName")
    anno_output_dir = ANNO_OUTPUT_PATH.format(project_name, '').replace('.json', '')
    fns = os.listdir(anno_output_dir)
    js = []
    for fn in fns:
        if not fn.endswith('.json'):
            continue
        js.append(read_txt_file(anno_output_dir + '/' + fn))
    anno_json_path = DOWNLOAD_FILE_LOCATION.format(project_name).replace('result.json', 'anno.json')
    open('app/'+anno_json_path, 'w', encoding='utf-8').write('\n'.join(js))
    response = make_response(send_from_directory(directory='', path=anno_json_path, as_attachment=True))
    response.headers["Content-disposition"] = 'attachment; filename=result.json'

    return response
