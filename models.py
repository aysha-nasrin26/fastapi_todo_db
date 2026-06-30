from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from database import Base
from sqlalchemy.orm import relationship

#db table representation
class Task(Base):
    #mysql tasks table
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    priority = Column(String(255), nullable= False)
    status = Column(String(255),nullable=False)
    deadline = Column(String(100), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

class User(Base):
     __tablename__ = "users"
     
     id = Column(Integer,primary_key=True, index=True)
     email = Column(String(255), nullable=False)
     hashed_password =  Column(String(255), nullable=False) 
     tasks = relationship("Task", back_populates="owner")