from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sub")
async def root():
    return {"message" : "No message"}

# 코드를 수정하는 경우 자동으로 re-loading 진행


'''
# re-loading 시 메세지 확인 

WARNING:  WatchFiles detected changes in 'main.py'. Reloading...   # 파일을 수정 후 저장할 경우, 자동 re-loading
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [95810]
INFO:     Started server process [95853]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

'''

# 참고 : velog.io/@munang/

# 설치 방법 
# pip install fastapi
# pip install unicorn

# 실행방법
# uvicorn main:app --reload

# 참고 : weareyoung8-8.tistory.com/4
# API : 어쩐 서버의 특정한 부분에 접속해서 그 안에 있는 데이터와 서비스를 이용할 수 있게 해주는 소프트웨어 도구
# REST : 네트워크를 통해서 컴퓨터들끼리 통신할 수 있게 해주는 아키텍처 스타일