from app.config.setting import PROJECT_NAME, FILE_NAME, PROJECTS, ANNO_OUTPUT_PATH
from app.entities.entities import ReturnInfo, AnnoContents, OutputAnno, QueryAnno
from app.libs.redprint import RedPrint

from flask import request
import json
import os

from app.libs.tools import read_txt_file, write_json, read_json_file, make_dir

api = RedPrint('anno')


@api.route('/create', methods=['POST'])
def create_anno():
    ret_info = ReturnInfo()
    try:
        param = request.get_json()
        project_name = param.get(PROJECT_NAME)
        file_name = param.get(FILE_NAME)
        anno_details = param.get('annoDetails')

        anno_cont = AnnoContents()
        anno_cont.fileName = file_name
        anno_cont.annoDetails = anno_details
        anno_cont.isAnno = True

        anno_output_path = ANNO_OUTPUT_PATH.format(project_name)

        # 判断路径是否存在
        if not os.path.exists(anno_output_path):
            write_json(anno_output_path, [anno_cont])
            ret_info.errCode = 0
        else:
            output_anno = OutputAnno()
            output_anno.all_anno = read_json_file(anno_output_path)
            output_anno.add_anno(anno_cont)

            write_json(anno_output_path, output_anno.all_anno)
            ret_info.errCode = 0

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)

    return json.dumps(ret_info, default=lambda o: o.__dict__)


@api.route('/query', methods=['GET'])
def query_anno():
    ret_info = ReturnInfo()
    try:
        project_name = request.args.get("projectName").strip()
        file_name = request.args.get("fileName").strip()

        file_path = PROJECTS + '/' + project_name + '/' + file_name
        file_content = read_txt_file(file_path)

        anno_output_path = ANNO_OUTPUT_PATH.format(project_name)
        output_anno = OutputAnno()
        output_anno.all_anno = read_json_file(anno_output_path)

        query_anno = QueryAnno()
        query_anno.fileContent = file_content
        query_anno.annoDetails = output_anno.get_anno(file_name)
        ret_info.info = query_anno

        ret_info.errCode = 0

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(ret_info, default=lambda o: o.__dict__)
