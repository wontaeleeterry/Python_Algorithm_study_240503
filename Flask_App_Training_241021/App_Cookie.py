# 참고 : https://m.blog.naver.com/shino1025/221355012951

from flask import Flask, render_template, make_response
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
      user = request.form['nm']
      resp = make_response("Cookie Setting Complete")
      resp.set_cookie('userID', user)
      return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'


# 쿠키와는 다르게 세션은 데이터 서버에 저장된다.
# 서버에서 관리된다는 점에서 안정성이 좋다.
# 플라스크에서 세션은 딕셔너리 형태로 저장된다. -> 키를 통해 해당 값을 불러올 수 있다.


# Cookie : 정보를 유지할 수 없는 Connectionless, Stateless의 성격을 가진
# HTTP의 단점을 해결하기 위한 개념
# 웹 서버가 브라우저에게 지시하며 사용자의 로컬 컴퓨터에 파일 또는 메모리에 
# 저장하는 작은 기록 정보 파일
# 파일에 담기 정보는 사용자가 사이트에 방문할 때마다 읽히고 수시로 새로운
# 정보로 바뀔 수 있음
# -> 웹 서버에서 response 할 때, 헤더에 쿠키를 담아서 전달하는 개념

# Session : 트래픽 문제와 Cookie를 변경하는 보안 이슈를 해결하기 위해 등장
# 일정 시간동안 사용자(브라우저)로부터 들어오는 일련의 요구를 하나의 상태로 보고
# 그 상태를 일정하게 유지시키는 기술
# 브라우저를 통해 웹서버에 접속한 시점 < - 접속해 있는 상태 -> 종료하여 연결을 끝내는 시점
# 웹 서버에 저장되는 쿠키(=세션 쿠키), 브라우저를 닫거나 세션을 삭제했을 때만
# 삭제되므로 쿠키보다 비교적 보안이 좋다.
