from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    priority: str
    status: str
    deadline: str | None = None
    
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    status: str
    deadline: str | None = None
    
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str
    priority: str
    status: str
    deadline: str | None = None
    
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        #TO help SQLAl obj(Task) convert to Pydantic model(Taskresponse)
        from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True