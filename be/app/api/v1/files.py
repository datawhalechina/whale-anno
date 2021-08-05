from ...config.setting import PROJECT_PATH, ANNO_OUTPUT_PATH, DOWNLOAD_FILE_LOCATION

from ...libs.redprint import RedPrint

from flask import request, send_file, Response, send_from_directory, make_response
import json
import os

from ...entities.entities import ReturnInfo, FileInfo
from ...libs.tools import read_json_file, read_txt_file, write_json
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

        file_names = os.listdir(PROJECT_PATH.format(project_name))
        if 'config.json' in file_names:
            file_names.remove('config.json')
        if 'anno.json' in file_names:
            file_names.remove('anno.json')

        anno_output_path = ANNO_OUTPUT_PATH.format(project_name)

        # 判断路径是否存在
        if not os.path.exists(anno_output_path):
            for file_name in file_names[(page_number - 1) * page_size: (page_number - 1) * page_size + page_size]:
                file_info = FileInfo()
                file_info.fileName = file_name
                file_info.isAnno = False
                ret_info.info.append(file_info)
                print(2)
        else:
            for file_name in sorted(file_names)[
                             (page_number - 1) * page_size: (page_number - 1) * page_size + page_size]:
                file_info = FileInfo()
                file_info.fileName = file_name

                for anno_info in read_json_file(anno_output_path):
                    if anno_info.get('fileName') == file_name:
                        file_info.isAnno = anno_info.get('isAnno')

                ret_info.info.append(file_info.__dict__)

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
        project_name = request.args.get("projectName")
        # current_filename = request.args.get("current_filename")
        download_json = []
        anno_data = read_json_file(PROJECT_PATH.format(project_name) + '/anno.json')
        print(len(anno_data))
        for item in anno_data:

            item_dict = {'file': item['fileName'],
                         'text': read_txt_file(PROJECT_PATH.format(project_name) + '/' + item['fileName']),
                         'labels': list(set([x['type'] for x in item["annoDetails"]]))}
            print(item_dict)
            download_json.append(item_dict)
            # for detail in item["annoDetails"]:
            #     label_set = set()
            #     label_set.add(detail['type'])
            #     item_dict['labels'] = list(label_set)
            # download_json.append(item_dict)
        # print(download_json)
    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(download_json, default=lambda o: o.__dict__)

@api.route('/get_json', methods=['GET'])
def get_json():
    ret_info = ReturnInfo()
    try:

        project_name = request.args.get("projectName")
        download_json = []
        anno_data = read_json_file(PROJECT_PATH.format(project_name) + '/anno.json')
        for item in anno_data:
            item_dict = {}
            item_dict['file'] = item['fileName']

            item_dict['text'] = read_txt_file(PROJECT_PATH.format(project_name) + '/' + item['fileName'])
            # 这一步来去掉anno.json中的isSmall
            for entity in item['annoDetails']:
                if 'isSmall' in entity:
                    entity.pop('isSmall')
            # 也可以用这种方式来实现
            # item['annoDetails'].pop('isSmall','0')
            item_dict['entity'] = item['annoDetails']
            download_json.append(item_dict)
        write_json(PROJECT_PATH.format(project_name) + '/result.json', download_json)

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)

    # 返回数据
    # 1.返回json格式的数据
    # ret_info.info = download_json
    # ret_info.errCode = 0
    # return json.dumps(ret_info, default=lambda o: o.__dict__)

    # 使用send_from_directory 或者使用send_file时要特别注意文件的路径，路径不对的话会报404
    # 本线默认目录时app下，所以不需要再加/app了，所以不能用PROJECT_PATH
    # 2.创建response对象返回数据
    # 使用response可以将result.json再删除掉
    response = make_response(send_from_directory(directory='', path=DOWNLOAD_FILE_LOCATION.format(project_name),
                                                 as_attachment=True))
    response.headers["Content-disposition"] = 'attachment; filename=result.json'

    # print(PROJECT_PATH.format(project_name)+'/result.json')
    # os.remove(PROJECT_PATH.format(project_name)+'/result.json')

    def delete():
        time.sleep(3)
        os.remove(PROJECT_PATH.format(project_name) + '/result.json')
        print('result.json has been deleted')

    thread = threading.Thread(target=delete)
    thread.start()
    return response

    # 3. 直接使用send from directory 返回json文件
    # return send_from_directory('', filename=DOWNLOAD_FILE_LOCATION.format(project_name),as_attachment=True)

    # 4. 使用send file 返回json文件
    # return send_file(DOWNLOAD_FILE_LOCATION.format(project_name), as_attachment=True, attachment_filename=project_name+'_result.json')
