from flask import Flask, request, jsonify                # Flask를 사용하기 위하여 임포트
# request - 엔드 포인트에 전송된 HTTP 요청 정보 (헤더, 바디)를 저장
#           HTTP 요청을 통해 전송한 JSON 데이터를 읽어 들일 수 있다.


app = Flask(__name__)                  # 임포트한 Flask 클래스를 객체화시켜 app이라는 변수에 자장 -> API 애플리케이션이 된다.
app.id_count = 1
app.users = {}


@app.route("/ping", methods=['GET'])   # route 데코레이터를 사용하여 함수(ping() 함수)들을 엔드포인트로 등록하는 방식을 사용
def ping():                            # ping 함수를 정의 - 단순히 "pong" 텍스트만을 리턴
    return "pong"

@app.route("/sign-up", methods=['POST'])   # POST 방식의 엔드포인트 : 'field = value' 추가
def sign_up():
    new_user = request.json           # HTTP 요청을 통해 전송된 회원 정보를 읽어들인다.
    new_user["id"] = app.id_count

    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)
#-----------------------------------------------------
# API 실행 방법 #

# set FLASK_APP=app_240907.py
# flask run

# http://127.0.0.1:5000/ping

#-----------------------------------------------------
# 윈도우에서 httpie 설치 : pip install -U httpie
# 커멘드 창에서 : http -v GET http://127.0.0.1:5000/ping


#(base) C:\Users\wonta>http -v GET http://127.0.0.1:5000/ping
#GET /ping HTTP/1.1
#Accept: */*
#Accept-Encoding: gzip, deflate, br, zstd
#Connection: keep-alive
#Host: 127.0.0.1:5000
#User-Agent: HTTPie/3.2.3



#HTTP/1.1 200 OK
#Connection: close
#Content-Length: 4
#Content-Type: text/html; charset=utf-8
#Date: Mon, 09 Sep 2024 07:59:25 GMT
#Server: Werkzeug/2.2.3 Python/3.11.7

#pong


#-----------------------------------------------------
# 커멘드 창에서 : http -v POST http://127.0.0.1:5000/sign-up name=Terry
#-----------------------------------------------------

#(base) C:\Users\wonta>http -v POST http://127.0.0.1:5000/sign-up name=Terry
#POST /sign-up HTTP/1.1
#Accept: application/json, */*;q=0.5
#Accept-Encoding: gzip, deflate, br, zstd
#Connection: keep-alive
#Content-Length: 17
#Content-Type: application/json
#Host: 127.0.0.1:5000
#User-Agent: HTTPie/3.2.3

#{
#    "name": "Terry"
#}


#HTTP/1.1 200 OK
#Connection: close
#Content-Length: 24
#Content-Type: application/json
#Date: Mon, 09 Sep 2024 07:58:18 GMT
#Server: Werkzeug/2.2.3 Python/3.11.7

#{
#    "id": 1,
#    "name": "Terry"


#(base) C:\Users\wonta>http -v POST http://127.0.0.1:5000/sign-up name=Terry email=wontae.lee@gmail.com
#POST /sign-up HTTP/1.1
#Accept: application/json, */*;q=0.5
#Accept-Encoding: gzip, deflate, br, zstd
#Connection: keep-alive
#Content-Length: 50
#Content-Type: application/json
#Host: 127.0.0.1:5000
#User-Agent: HTTPie/3.2.3

#{
#    "email": "wontae.lee@gmail.com",
#    "name": "Terry"
#}


#HTTP/1.1 200 OK
#Connection: close
#Content-Length: 55
#Content-Type: application/json
#Date: Mon, 09 Sep 2024 08:01:31 GMT
#Server: Werkzeug/2.2.3 Python/3.11.7

#{
#    "email": "wontae.lee@gmail.com",
#    "id": 1,
#    "name": "Terry"
#}