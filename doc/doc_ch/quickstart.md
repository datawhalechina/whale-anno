# 快速开始
## 一、环境配置
请参考[环境配置](./installation.md)配置whale-anno运行环境。
## 二、启动项目
### 1、启动后端
打开命令行（Windows中的打开方式：进入项目目录，按住键盘上的shift，然后右键，选择在【在此处打开 PowerShell 窗口(S)】）
```shell
# 进入后端目录
cd ./be
# 启动后端脚本
python3 ./run.py
```
*此时项目的后端会被启动在http://localhost:9060/*
### 2、启动前端
用上述方法，打开一个新的命令行
```shell
# 进入前端
cd ./fe
# 启动前端页面
npm run start
```
*此时项目的前端会被启动在http://localhost:8080/*
## 三、开始使用
打开上述前端页面地址，然后请参考[快速使用](./quickuse.md)。
