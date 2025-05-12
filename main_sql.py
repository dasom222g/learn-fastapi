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

@app.get('/mysqltest')
def mysqltest(request: Request):
  query = db_connection.execute('select * from player')
  result_db = query.fetchall()

  result = []
  for data in result_db:
    item = {'player_id': data[0], 'player_name': data[1]}
    result.append(item)

  return templates.TemplateResponse('sql-test.html', {'request': request, 'result_list': result})

# 쿼리 방식
@app.get('/detail')
def test_post(request: Request, id: str, name: str):
    print(id, name)
    # SQL Injection 방지를 위해 바인딩 처리
    # select * from player where player_name like '_준'; 
    query = db_connection.execute(f"SELECT player_id, player_name, team_id, height, weight FROM player WHERE player_id={id} and player_name like '%%{name}%%'")
    result_db = query.fetchall()
    result = []
    for i in result_db:
        temp = {
            'player_id': i[0],
            'player_name': i[1],
            'team_name': i[2],
            'height': i[3],
            'weight': i[4]
        }
        result.append(temp)
    return templates.TemplateResponse("detail.html", {"request": request, "result_list": result})

@app.post("/update")
def post_update(request: Request, id:str, name:str, pname: Annotated[str, Form()], tname: Annotated[str, Form()], weight: Annotated[str, Form()], height: Annotated[str, Form()]):
    if pname != '':
        db_connection.execute("update player set player_name = '{}' where player_id = {} and player_name like '{}' ".format(pname,id,name))
        name = pname
    if tname != '':
        db_connection.execute("update player set team_id = '{}' where player_id = {} and player_name like '{}' ".format(tname,id,name))
    if weight != '':
        query = db_connection.execute("update player set weight = {} where player_id = {} and player_name like '{}' ".format(weight,id,name))
    if height != '':
        query = db_connection.execute("update player set height = {} where player_id = {} and player_name like '{}' ".format(height,id,name))
    # 다시불러오기
    query = db_connection.execute(f"select * from player where player_id = {id} and player_name like '{name}'")
    result_db = query.fetchall()
    result = []
    for i in result_db:   # i는 ('2012136', '오비나', 'K10', '', '', '', 'MF', 26, '', datetime.date(1990, 6, 3), '1', 169, 70) 들어옴
        temp = {'player_id':i[0],'player_name':i[1],'team_name':i[2],'height':i[-2],'weight':i[-1] }
        result.append(temp)
    return templates.TemplateResponse("detail.html", {'request': request,'result_list':result}) 

@app.get("/delete")
def deletetest(request: Request, id:str, name:str):
    db_connection.execute(f"delete from player where player_id = {id} and player_name like '{name}'")
    # 삭제 후 목록들 다시가져오기
    query = db_connection.execute("select * from player")
    result_db = query.fetchall()
    result = []
    for i in result_db:   # i는 ('2012136', '오비나', 'K10', '', '', '', 'MF', 26, '', datetime.date(1990, 6, 3), '1', 169, 70) 들어옴
        temp = {'player_id':i[0],'player_name':i[1] }
        result.append(temp)
    return templates.TemplateResponse('sql-test.html',{'request': request,'result_list':result})


if __name__ == '__main__':
  print('서버on')
  uvicorn.run(app, host='localhost', port=8080)
  