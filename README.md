# whaleAnno
Datawhale自研数据标注工具

## Demo
https://tekii.cn/ner

## 快速开始
### 1.环境配置
#### 下载所需软件
##### Python 3
经测试whaleAnno后端代码可在Python 3.7.9上运行，您也可以测试其他版本，一般建议安装最新版

##### Node.js
经测试whaleAnno前端代码可在Node.js v12.16.3上运行，在Node.js v8.10.0安装本地调试工具失败，您也可以测试其他版本，一般建议安装最新版

#### 克隆项目
```shell
git clone https://github.com/datawhalechina/whale-anno.git
```
#### 下载依赖
##### 下载后端依赖
```shell
# 下载后端依赖
python3 -m pip install flask
```
后端只依赖了flask这个第三方库

##### 下载前端依赖
```shell
# 进入前端文件夹
cd ./fe
# 下载前端依赖
npm install
```
npm为Node.js安装以后自带的包管理工具

### 2.启动项目
#### 启动后端
打开终端
```shell
# 进入后端目录
cd ./be
# 启动后端脚本
python3 ./run.py
```
此时项目的后端会被启动在http://localhost:9060

#### 启动前端
用上述方法，打开一个新的命令行
```shell
# 进入前端
cd ./fe
# 启动前端页面
npm run start
```
此时项目的前端会被启动在http://localhost:8080

### 3.开始使用
打开上述前端页面地址（http://localhost:8080），然后请参考[使用说明](./doc/README.md)开始使用。


## 开发团队
| 职责 | 名单 |
| :---: | :---: |
| **PM** | [谢文睿](https://github.com/Sm1les) |
| **前端** | [马琦钧](https://github.com/Skypow2012) |
| **后端** | 付文豪 |

## 关注我们
<div align=center>
<img src="https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg" width = "250" height = "270" alt="Datawhale是一个专注AI领域的开源组织，以“for the learner，和学习者一起成长”为愿景，构建对学习者最有价值的开源学习社区。关注我们，一起学习成长。">
</div>