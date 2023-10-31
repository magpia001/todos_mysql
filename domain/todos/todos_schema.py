from pydantic import BaseModel, validator

class Todo(BaseModel):
    id: int
    task: str
    completed: bool

    class Config:
        orm_mode = True

# Todo 리스트 스키마
class TodoList(BaseModel):
    todo_list: list[Todo] = []

# Todo 추가 스키마
class TodoAdd(BaseModel):
    task: str

    @validator('task')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
# Todo 수정 스키마
class TodoUpdate(Todo):
    pass

# Todo 삭제 시키마
class TodoDelete(BaseModel):
    todo_id: int



