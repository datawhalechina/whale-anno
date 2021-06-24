import requests
import json
import threading

headers = {'Content-Type': 'application/json'}
data = {"projectName":"demo5","fileName":"test11.txt","annoDetails":[{"name":"北","type":"person1","start":5,"end":6,"isSmall":False}]}
test_times = 20
test_cnt = 0
err_cnt = 0

def create_load():
    global test_times
    global test_cnt
    global err_cnt
    result = requests.post('http://127.0.0.1:9060/v1/anno/create', data=json.dumps(data), headers=headers)
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
    t = threading.Thread(target=create_load,args=())
    t.start()
