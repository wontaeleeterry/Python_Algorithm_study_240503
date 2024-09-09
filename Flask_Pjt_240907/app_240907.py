from flask import Flask                # Flask를 사용하기 위하여 임포트
 
app = Flask(__name__)                  # 임포트한 Flask 클래스를 객체화시켜 app이라는 변수에 자장 -> API 애플리케이션이 된다.

@app.route("/ping", methods=['GET'])   # route 데코레이터를 사용하여 함수(ping() 함수)들을 엔드포인트로 등록하는 방식을 사용
def ping():                            # ping 함수를 정의 - 단순히 "pong" 텍스트만을 리턴
    return "pong"




#-----------------------------------------------------
# API 실행 방법 #

# set FLASK_APP=app_240907.py
# flask run

# http://127.0.0.1:5000/ping

#-----------------------------------------------------
# 윈도우에서 httpie 설치 : pip install -U httpie
# 커멘드 창에서 : http -v GET http://127.0.0.1:5000/ping
#-----------------------------------------------------

'''
# GET 메소드
: POST 메소드와 함께 가장 많이 사용하는 메소드
: 이름 그대로 어떠한 데이터를 서버로부터 요청(GET)할 때 주로 사용하는 메소드
: 데이터의 생성이나 수정 그리고 삭제 등의 변경 사항이 없이 단순히 데이터를 받아오는 요청
: body가 비어있는 경우가 많다.

(base) C:\Users\wonta>http -v GET http://127.0.0.1:5000/ping
GET /ping HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Host: 127.0.0.1:5000
User-Agent: HTTPie/3.2.3



HTTP/1.1 200 OK                              # HTTP의 응답 메시지의 구조 - Status Line :응답 메시지의 상태를 간략히 요약
Connection: close                            # HTTP의 응답 메시지의 구조 - Headers
Content-Length: 4
Content-Type: text/html; charset=utf-8
Date: Mon, 09 Sep 2024 07:17:45 GMT          # HTTP의 응답 메시지의 구조 - Body : 이하 HTML 파일의 헤더를 포함한 내용들
Server: Werkzeug/2.2.3 Python/3.11.7

pong

'''

'''
--------------------------------------------------------------
# How to Design Beautiful REST API!
# https://www.youtube.com/watch?v=4DxHX95Lq2U
--------------------------------------------------------------
# API 엔드포인트 아키텍처 패턴
- REST 방식
- GraphQL (페이스북이 개발, 비교적 최근에 나온 기술)

REST(Representation State Transfer)ful HTTP API
: API 시스템을 구현하기 위한 아키텍처의 한 형식
: API에 전송하는 리소스(resource)를 URI로 표현하고,
헤당 리소스에 행하고자 하는 의도를 HTTP 메소드로 정의하는 방식


'''