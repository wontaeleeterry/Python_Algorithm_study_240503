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

'''
참고 : https://emilkwak.github.io/python-setting-file-ext

설정을 저장하는데 어떤 포맷을 쓰는가에 따라 설정 파일 확장자만 바뀌는게 아니라,
설정 항목들이 표현되는 형식이 달라지고 나아가 이 항목들이 파일을 이루는 형태도 달라진다.

*설정에 해당할 수 있는 사항의 예:

접속정보 (서버 IP 주소, 포트 번호 등)
각종 모드(운영, 개발, 시뮬레이션 등)
언어(한국어, 영어, 독일어)
제어값(업로드 용량 상한, 동시 처리량 등)
경로(아이콘 이미지, 데이터 파일 등)
기타
'''