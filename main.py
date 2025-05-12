from typing import Annotated

from sqlalchemy import create_engine
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# FastAPI클래스로 웹 객체(인스턴스) 만듬
templates = Jinja2Templates(directory="templates")
app = FastAPI() # 클래스


# MySQL 데이터베이스 연결 객체 생성
db_connection = create_engine('mysql://test:1234@127.0.0.1:3306/test') # test 사용자, 비밀번호 1234로 localhost의 test 데이터베이스에 연결
query = db_connection.execute('select * from player') # SQL 쿼리 실행: execute메서드는 SQL문 실행후 ResultProxy 객체 반환
result = query.fetchall() # 모든 결과 행을 한 번에 가져와 튜플 리스트로 반환

# for data in result:
#   print('data', data)


@app.get('/register')
def get_register(request: Request):
  return templates.TemplateResponse('register.html', {'request': request})

@app.post('/register')
def get_register(request: Request, sname: Annotated[str, Form()], s_id: Annotated[str, Form()], s_pwd: Annotated[str, Form()], email: Annotated[str, Form()]):
  print(f'sname: {sname} s_id: {s_id} s_pwd: {s_pwd}, email: {email}')
  # DB에 추가
  db_connection.execute(f"insert into student(sname, s_id, s_pwd, email) values('{sname}', '{s_id}', '{s_pwd}', '{email}')")

  return templates.TemplateResponse('login.html', {'request': request})

@app.get('/login')
def getLogin(request: Request):
  return templates.TemplateResponse('login.html', {'request': request, 'message': ''})

@app.post('/sign-in')
def postSignIn(request: Request, s_id: Annotated[str, Form()], s_pwd: Annotated[str, Form()]):
  get_query = db_connection.execute(f"select sname from student where s_id='{s_id}' and s_pwd like '{s_pwd}'")
  result = get_query.fetchall() # 빈 list or 튜플로 이루어진 리스트
  print('result_list', result)
  
  message = ''
  if len(result) > 0:
    name = result[0][0]
    message = f'{name}님 반갑습니다!'
  else:
    message = '존재하지 않는 회원입니다.'
  
  return templates.TemplateResponse('login.html', {'request': request, 'message': message}) 



if __name__ == '__main__':
  print('서버on')
  uvicorn.run(app, host='localhost', port=8080)
