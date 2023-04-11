from app.config.setting import PROJECT_NAME, FILE_NAME, PROJECT_PATH, ANNO_OUTPUT_PATH
from app.entities.entities import ReturnInfo, AnnoContents, OutputAnno, QueryAnno
from app.libs.redprint import RedPrint
import time
from flask import request
import json
import os
import zipfile

from ...libs.tools import read_file, write_json, read_json_file, make_dir

api = RedPrint('anno')

waiting_list_dic = {}

@api.route('/create', methods=['POST'])
def create_anno():
    ret_info = ReturnInfo()
    try:
        j = request.get_json()
        anno_output_path = ANNO_OUTPUT_PATH.format(j["projectName"], j["fileName"])
        with open(anno_output_path, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(request.get_json(), ensure_ascii=False))

    except Exception as e:
        print(e)
        ret_info.errCode = 404
        ret_info.errMsg = str(e)

    return json.dumps(ret_info, default=lambda o: o.__dict__)


@api.route('/query', methods=['GET'])
def query_anno():
    ret_info = ReturnInfo()
    try:
        project_name = request.args.get("projectName").strip()
        file_name = request.args.get("fileName").strip()

        file_path = PROJECT_PATH.format(project_name) + '/' + file_name
        file_content = read_file(file_path)

        anno_output_path = ANNO_OUTPUT_PATH.format(project_name, file_name)
        anno_details = []
        if os.path.exists(anno_output_path):
            anno_details = json.loads(read_file(anno_output_path))['annoDetails']

        query_anno = QueryAnno()
        query_anno.fileContent = file_content
        query_anno.annoDetails = anno_details
        ret_info.info = query_anno

        ret_info.errCode = 0

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(ret_info, default=lambda o: o.__dict__)
