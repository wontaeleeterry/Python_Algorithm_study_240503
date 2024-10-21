# 실시간 시간 출력 
# Jinja2 - html 연결
# 일정 시간 주기로 내용 갱신 등

from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sample_secret'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    now = datetime.now()    # 현재 시각을 전달하고
    name = now              # Jinja2 구문을 통하여 현재 시각을 실시간으로 전달
    return render_template('hello.html', name = name)

# 파이썬의 name 변수를 html의 {{name}} 으로 전달 (데이터 던져주기)