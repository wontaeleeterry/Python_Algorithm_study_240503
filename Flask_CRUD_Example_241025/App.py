# 코드 출처 : https://youngminieo1005.tistory.com/93

from flask import Flask, render_template, request, url_for, redirect
import sqlite3 # salite3
 
app = Flask(__name__)
conn = sqlite3.connect("database.db")   # splite3 db 연결 / 해당 파일이 없는 경우 새로 생성됨
print("Opened database successfully")
conn.execute("CREATE TABLE IF NOT EXISTS Board(name TEXT, context TEXT)")   # Board 라는 DB생성
print("TABLE Created Successfully")

'''
# 비어 있는 데이터 베이스 유지

name = [
    ["Elice", 15],
    ["Dodo", 16],
    ["checher", 17],
    ["Queen", 18]
]

for i in range(len(name)):
    conn.execute(f"INSERT INTO Board(name,context) VALUES('{name[i][0]}', '{name[i][1]}')")  # Board DB에 데이터 삽입

'''


conn.commit()   # 지금껏 작성한 SQL, DB에 반영 commit
conn.close()    # 작성 다한 DB는 닫아줘야함 close
 
# ================= 여기서부터는 다시 Flask 영역 ==========================
 
@app.route('/')
def board():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Board")
    rows = cur.fetchall()
 
    print("DB: ")
    for i in range(len(rows)):
        print(rows[i][0] + ':' + rows[i][1])
    return render_template("board1.html", rows = rows)
 
 
@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        name = request.form["name"] # search.html 가보면, form에 name만 받기로 함.
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Board WHERE name='{name}'")
        rows = cur.fetchall()
        print("DB : ")
        for i in range(len(rows)):
            print(rows[i][0] + ':' + rows[i][1])
        return render_template("search.html", rows=rows)
    else:
        return render_template("search.html")
 
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        try:
            name = request.form["name"]
            context = request.form["context"]
 
            # DB에 접근해서, 데이터를 삽입할때는, 직접 DB를 열어야되는데, 윗 과정처럼, close까지 하기 힘드니깐, 하는 방식, 결과는 같은 것 !
            # with문의 범위를 벗어나면서 파일 객체 f가 자동으로 close() 되기 때문
            # --> 실제로는 __exit__()한다 라고 정의해야 한다.
            # 참고 : https://emilkwak.github.io/with-statement

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Board(name,context) VALUES('{name}','{context}')")
                con.commit()
        except:
            con.rollback()  # DB 롤백함수, SQL이 오류나면, 반영전, 이전 상태로 돌리는 것
        finally:
            return redirect(url_for("board"))
    else:
        return render_template("add.html")
 
 
if __name__ == '__main__':
    app.run()