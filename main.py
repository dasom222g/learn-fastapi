from fastapi import FastAPI, Request # 클랙스
from fastapi.templating import Jinja2Templates
import uvicorn

# FastAPI클래스로 웹 객체(인스턴스) 만듬
templates = Jinja2Templates(directory="templates")
app = FastAPI()


# 웹 객체에 path넣어주면 아래 함수 실행됨
@app.get('/blog')
def hello():
  return {"message": "Hello world"}


@app.get('/test')
def test(request: Request):
  print('request!!')
  print(request)

  return templates.TemplateResponse('test.html', {'request': request, 'a': 2})

# python3 main.py만 실행해도 [uvicorn main:app --reload]로 서버 띄우게끔 세팅
if __name__ == '__main__':
  print('서버on')
  uvicorn.run(app, host='localhost', port=8080)
  