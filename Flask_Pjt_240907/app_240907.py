from flask import Flask                # Flask를 사용하기 위하여 임포트
 
app = Flask(__name__)                  # 임포트한 Flask 클래스를 객체화시켜 app이라는 변수에 자장 -> API 애플리케이션이 된다.

@app.route("/ping", methods=['GET'])   # route 데코레이터를 사용하여 함수(ping() 함수)들을 엔드포인트로 등록하는 방식을 사용
def ping():                            # ping 함수를 정의 - 단순히 "pong" 텍스트만을 리턴
    return "pong"

# API 실행 방법 #

# set FLASK_APP=app_240907.py
# flask run

# http://1270.0.1:5000/ping