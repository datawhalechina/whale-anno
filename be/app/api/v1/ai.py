from app.libs.redprint import RedPrint
import time
from flask import request
import json
import os

from ...libs.tools import read_file, write_json, read_json_file, make_dir

import auto_anno_2 as aa

api = RedPrint('ai')

class ReturnInfo:
    def __init__(self):
        self.errCode = 0
        self.errMsg = ''
        self.info = []

@api.route('/nlp/cls', methods=['POST'])
def nlp_cls():
    ret_info = ReturnInfo()
    try:
        j = request.get_json()
        texts = j['texts']
        types = j['types']
        annos = []
        for text in texts:
            anno = aa.cls(text, types)
            annos.append(anno)
        ret_info.info = annos
    except Exception as e:
        print(e)
        ret_info.errCode = 404
        ret_info.errMsg = str(e) 

    return ret_info.__dict__

@api.route('/nlp/ner', methods=['POST'])
def nlp_ner():
    ret_info = ReturnInfo()
    try:
        j = request.get_json()
        texts = j['texts']
        types = j['types']
        annos = []
        for text in texts:
            anno = aa.ner(text, types)
            annos.append(anno)
        ret_info.info = annos
    except Exception as e:
        print(e)
        ret_info.errCode = 404
        ret_info.errMsg = str(e) 

    return ret_info.__dict__
