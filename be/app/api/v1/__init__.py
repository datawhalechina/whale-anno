from flask import Blueprint
from ...api.v1 import index, project, files, anno, ai


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    index.api.register(bp_v1, url_prefix='/index')
    project.api.register(bp_v1, url_prefix='/project')
    anno.api.register(bp_v1, url_prefix='/anno')
    files.api.register(bp_v1, url_prefix='/files')
    ai.api.register(bp_v1, url_prefix='/ai')

    return bp_v1
