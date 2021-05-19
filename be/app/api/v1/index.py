from app.config.setting import PROJECTS, PROJECT_CONFIG_PATH
from app.entities.entities import ReturnInfo
from app.libs.redprint import RedPrint
import json
import os

from app.libs.tools import read_json_file

api = RedPrint('index')


# 访问首页 http://localhost:9060/v1/index
# @api.route('/index')
@api.route('', methods=['GET'])
def index():
    # 打开项首页时，返回我的项目信息
    ret_info = ReturnInfo()
    try:
        project_config_info = []
        for project_name in os.listdir(PROJECTS):
            project_config_name = PROJECT_CONFIG_PATH.format(project_name)
            print(project_config_name)
            if os.path.exists(project_config_name):
                project_config_info.append(read_json_file(project_config_name))

        ret_info.errCode = 0
        ret_info.info = project_config_info
    except Exception as e:
        ret_info.errCode = 404
        ret_info.errMsg = str(e)

    return json.dumps(ret_info, default=lambda o: o.__dict__)
