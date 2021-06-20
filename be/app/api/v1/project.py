from app.config.setting import PROJECT_NAME, PROJECT_TYPE, ENTITY_TYPES, PROJECTS, PROJECT_PATH, PROJECT_CONFIG_PATH, \
    ANNO_OUTPUT_PATH
from app.libs.redprint import RedPrint

from flask import request
import json
import os
from app.libs.tools import make_dir, write_json, read_json_file
from app.entities.entities import Project, ReturnInfo

api = RedPrint('project')


@api.route('/create', methods=['POST'])
def create_project():
    ret_info = ReturnInfo()
    try:
        param = request.get_json()
        project_name = param.get(PROJECT_NAME)

        make_dir(PROJECT_PATH.format(project_name))
        write_json(PROJECT_CONFIG_PATH.format(project_name), param)
        anno_path = ANNO_OUTPUT_PATH.format(project_name)
        if not os.path.exists(anno_path):
            write_json(anno_path, [])

        ret_info.errCode = 0

    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)
    return json.dumps(ret_info, ensure_ascii=False, default=lambda o: o.__dict__)


@api.route('/update_entity_types', methods=['POST'])
def update_entity_types():
    ret_info = ReturnInfo()
    try:
        param = request.get_json()
        project_name = param.get(PROJECT_NAME)
        entity_types = param.get(ENTITY_TYPES)
        print(entity_types)

        new_entity_types = []
        for entity_type in entity_types:
            new_entity_types.append(entity_type.get('type'))

        anno_output_path = ANNO_OUTPUT_PATH.format(project_name)

        if os.path.exists(PROJECT_CONFIG_PATH.format(project_name)):  # False
            project_config_info = read_json_file(PROJECT_CONFIG_PATH.format(project_name))
            project = Project()
            project.projectName = project_config_info.get(PROJECT_NAME)
            project.projectType = project_config_info.get(PROJECT_TYPE)
            project.entityTypes = entity_types
            print(project.entityTypes)

            if os.path.exists(anno_output_path):
                anno_details = read_json_file(anno_output_path)
                for anno_info in anno_details:
                    anno_detail = json.loads(anno_info.get('annoDetails'))
                    for ind, anno in enumerate(anno_detail):
                        entity_type = anno.get('type')
                        if entity_type not in new_entity_types:
                            anno_detail.pop(ind)
                write_json(anno_output_path, anno_details)

            write_json(PROJECT_CONFIG_PATH.format(project_name), project)
            ret_info.errMsg = 'update ok'

        ret_info.errCode = 0
    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)

    return json.dumps(ret_info, default=lambda o: o.__dict__)
