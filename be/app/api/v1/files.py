from app.config.setting import PROJECT_PATH, ANNO_OUTPUT_PATH
from app.libs.redprint import RedPrint

from flask import request
import json
import os

from app.entities.entities import ReturnInfo, FileInfo
from app.libs.tools import read_json_file

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
            for file_name in sorted(file_names)[(page_number - 1) * page_size: (page_number - 1) * page_size + page_size]:
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
