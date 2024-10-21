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

