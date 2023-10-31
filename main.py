""" 
simple todo
fastAPI를 활용한 DB CRUD
명령 실행 : 
  - uvicorn main:app --reload
  또는
  - python app_start.py
"""
# main.py
from typing import List
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from database import engine, sessionlocal
from sqlalchemy.orm import Session
import models

from domain.todos import todos_schema

# frontend build파일 적용시 필요
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI() 객체 생성
app = FastAPI()

# 서버사이드 data rendering 시 필요한 설정
## html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
## templates = Jinja2Templates(directory="templates")
## static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173/",
    # "http://127.0.0.1:5173/",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    # origins를 다음과 같이 넣으면 해결됨
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

def get_db():
    db = sessionlocal()
    try:
        # yield 키워드는 FastAPI가 함수의 실행을 일시 중지하고 데이터베이스 세션을 호출자에게 반환하도록 지시
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

# frontend build 후 홈 path 적용
@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

@app.get("/todo/list", response_model=List[todos_schema.Todo])
def home(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    # print(todos.count())
    # print(todos)
    # for todo in todos:
    #     print(todo)
    # if todos.count() == 0:
    #     todos = 0
    return list(todos)
    

# todo 추가
@app.post("/todo/add", status_code=status.HTTP_201_CREATED)
def add(todo: todos_schema.TodoAdd, db: Session = Depends(get_db)):
    print(todo.task)
    todo = models.Todo(task=todo.task)
    db.add(todo)
    db.commit()

# 수정할 todo 조회 처리
@app.get("/todo/edit/{todo_id}", response_model=todos_schema.Todo, status_code=status.HTTP_200_OK)
def edit(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    # print(todo)
    return todo

# 수정 todo update 처리
@app.put("/todo/update")
# 클라이언트에서 넘온 데이터 타입 정의
# todo_update: todos_schema.TodoUpdate
# 데이터 받는 변수 : 데이터 타입
def edit(todo_update: todos_schema.TodoUpdate, db: Session = Depends(get_db)):
    # 수정할 레코드 조회하기
    todo = db.query(models.Todo).filter(models.Todo.id == todo_update.id).first()
    print(todo_update.task)
    print(todo)
    # 수정할 값 적용하기
    todo.task = todo_update.task
    todo.completed = todo_update.completed
    db.commit()

# todo 삭제 처리
@app.get("/todo/delete/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit() 


