# API文档

| url                        | methods | params                                                   | return                           |
| -------------------------- | ------- | -------------------------------------------------------- | -------------------------------- |
| v1/project/get_zipped_data | POST    | projectName:项目名 file:数据集文件（目前只支持.zip格式） | json ：errcode表示是否成功导入   |
| v1/files/get_json          | GET     | projectName:项目名                                       | file（.json格式的数据集标注结果） |
|v1/project/delete_program   |GET      |projectName:项目名|json：errcode表示是否成功|
| v1/files//get_labels       | GET     | projectName:项目名                                       | file（.json格式的数据集标注结果） |

