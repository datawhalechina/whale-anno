import requests
import json
import threading
import time
import random
headers = {'Content-Type': 'application/json', 'Connection': 'close'}
data = {"projectName": "demo5", "fileName": "test11.txt",
        "annoDetails": [{"name": "北", "type": "person1", "start": 5, "end": 6, "isSmall": False}]}
test_times = 1000
test_cnt = 0
err_cnt = 0
requests.DEFAULT_RETRIES = 1000

requests.adapters.DEFAULT_RETRIES = 1000
s = requests.session()
s.keep_alive = False


def create_load():
    global test_times
    global test_cnt
    global err_cnt
    global s
    result = requests.post('http://127.0.0.1:9060/v1/anno/create', data=json.dumps(data), headers=headers, timeout=30)

    print(result.text)
    if result.json()['errMsg']:
        err_cnt += 1
        print('Catch Err:', result.json())
    test_cnt += 1
    if test_cnt == test_times:
        if err_cnt == 0:
            print('Test success!')
        else:
            print('Test failed!')


print('Start', test_times, 'test')
for i in range(test_times):
    # 单线程测试
    # create_load()
    # 多线程测试
    time.sleep(random.randint(100,200)*0.0001)
    t = threading.Thread(target=create_load, args=())
    # t.setDaemon(True)
    t.start()
time.sleep(1)
print("ERROR COUNT"+str(err_cnt))
# print("OK")
