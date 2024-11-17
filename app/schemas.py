from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    active: bool

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int
    active: bool

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id: int
    completed: bool
    active: bool

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id: int
    completed: bool
    active: bool
