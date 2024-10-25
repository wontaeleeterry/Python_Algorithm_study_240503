import json

# 파일이 실행되는 경로 직접 확인하는 방법
import os
print(os.getcwd())

# 파일 경로 입력 시 주의 '/'로 입력해야 한다. (241024)
# c:\Users\wonta\My_github\Python_Algorithm_study_240503\Flask_CRUD_Example_241025\config_example\

with open('c:/Users/wonta/My_github/Python_Algorithm_study_240503/Flask_CRUD_Example_241025/config_example/config.json') as f:
# with open('config.json') as f:   # 왜 경로 에러가 발생하는가? 전체 경로를 모두 입력해야 하는가?
    config = json.load(f)
print(config['2nd_key'])    # vlaue_last