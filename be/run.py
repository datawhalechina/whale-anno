# 入口程序文件
from app.app import create_app

app = create_app()

# host='0.0.0.0'
#     本机访问: 将浏览器中0.0.0.0替换成127.0.0.1 或 localhost
#     内网访问: 将浏览器中0.0.0.0替换成运行程序的ip地址
# port='9060'    可自己指定端口

# 例: 访问首页 http://localhost:9060/v1/index
# localhost是ip
# 9060是端口
# v1是版本
# index是首页
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9060, debug=True)