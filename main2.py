from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# FastAPI클래스로 웹 객체(인스턴스) 만듬
templates = Jinja2Templates(directory="templates")
app = FastAPI() # 클랙스
# static폴더 연결
app.mount('static', StaticFiles(directory='static'), name='static')


# 웹 객체에 path넣어주면 아래 함수 실행됨
@app.get('/blog')
def hello():
  return {"message": "Hello world"}


@app.get('/test')
def test(request: Request):
  print('request----------')
  # print(request)  # request 전체 객체 출력
  # print(request.body())  # 요청 body 출력 (POST/PUT 등)
  # print(request.method)  # GET, POST 등
  # print(request.url)     # 요청 URL
  # print(request.headers) # 요청 헤더
  # print(request.cookies) # 요청 쿠키
  print('request----------')

  return templates.TemplateResponse('test.html', {'request': request, 'a': 2})

# 경로 파라미터
@app.get('/test/{name}')
def arg_print(request: Request, name: str, age: int):
  # name은 문자열로 형변환, age는 숫자로 형변환하여 받음
  print(f'name: {name}')
  return templates.TemplateResponse('test.html', {'request': request, 'a': 2})

# 쿼리 파라미터
@app.get('/test2')
def arg_print(request: Request, name: str, age: str):
  print(f'name: {name} age: {age}')
  return templates.TemplateResponse('test.html', {'request': request, 'a': 2})

# test2.html 전송
@app.get('/front_get')
def send_frontend(request: Request, name: str, age: str):
  return templates.TemplateResponse('test2.html', {'request': request, 'name': name, 'age': age})

# post_test.html 전송
@app.get('/post_page')
def post_page(request: Request):
  return templates.TemplateResponse('post_test.html', {'request': request})

# form타입의 사용자 입력값 가져오기
@app.post('/test_post')
def test_post(name: Annotated[str, Form()], pwd: Annotated[int, Form()]):
  print(name, pwd)

# python3 main.py만 실행해도 [uvicorn main:app --reload]로 서버 띄우게끔 세팅
if __name__ == '__main__':
  print('서버on')
  uvicorn.run(app, host='localhost', port=8080)
  