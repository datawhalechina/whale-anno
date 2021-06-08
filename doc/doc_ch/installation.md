# 环境配置
## 一、下载所需软件
### 1、Python 3
经测试Whale-anno后端代码可在Python 3.7.9上运行，您也可以测试其他版本，一般建议安装最新版
[Python 3官网下载地址](https://www.python.org/downloads/)
### 2、Node.js
经测试Whale-anno前端代码可在Node.js v12.16.3上运行，在Node.js v8.10.0安装本地调试工具失败，您也可以测试其他版本，一般建议安装最新版
[Node.js官网下载地址](https://nodejs.org/zh-cn/download/)
## 二、克隆项目
```shell
git clone https://github.com/datawhalechina/whale-anno.git
```
## 三、下载依赖
### 1、下载后端依赖
```shell
# 下载后端依赖
python3 -m pip install flask
```
*后端只依赖了flask这个第三方库*
### 2、下载前端依赖
```shell
# 进入前端文件夹
cd ./fe
# 下载前端依赖
npm install
```
*npm为Node.js安装以后自带的包管理工具*
