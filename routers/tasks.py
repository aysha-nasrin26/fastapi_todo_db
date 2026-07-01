from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Task, User
from routers.auth import get_current_user
from schemas import TaskCreate, TaskResponse, TaskUpdate


task_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

#task Added
@task_router.post("/tasks")
#def create_task(task: TaskCreate, db: Session = Depends(get_db)):
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
#db connection open and it using to execyte query,insert data,upd & dlt
    #db = SessionLocal()
    
    new_task = Task(
    title=task.title,
    priority=task.priority,
    status=task.status,
    deadline=task.deadline,
    owner_id=current_user.id
)

#pydantic object data SQL alchemy convert to task obj model
   #new_task = Task(
    #   title=task.title,
    #   priority=task.priority,
    #   status=task.status

#ready to save
    db.add(new_task)
#saved permanent
    db.commit()
#db close
   # db.close()

    return {
        "message": "Task Added Successfully"
    }
    
#task read
#return list of task
@task_router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    #pagination
    page: int = 1,
    limit: int = 10,
    search: str = "",#search query
    sort: str = "id",#sorting
    status: str | None = None,#filtering
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):
    
    # Create query
    query = db.query(Task)
    
    query = query.filter( 
        Task.owner_id == current_user.id#owenr filter
)
    #search filter
    if search:
        query = query.filter(
            Task.title.like(f"%{search}%")
    )
    #filtering pending tsk only
    if status:
        query = query.filter(
        Task.status == status
    )
    #sort=title (-title ascend A-Z or descend Z-A)
    if sort.startswith("-"):
        field = sort[1:]

        if hasattr(Task, field):
            query = query.order_by(
                getattr(Task, field).desc()
        )
    else:
        if hasattr(Task, sort):
            query = query.order_by(
                getattr(Task, sort)
        )
    #pagination
    skip = (page - 1) * limit
    #return
    return query.offset(skip).limit(limit).all()
#query start to Task tbl
#.all-tbl le ule all rows a lst aa kontu varum
    #tasks = db.query(Task).all()
    #SELECT*FROM tasks;
    #db.close()
    
#fetched data converted into json and its send back to the user 
    #return tasks
#Task Statistics API
@task_router.get("/tasks/stats")
def task_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):#Count Total Tasks
    total = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).count()
    #Count Pending
    pending = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.status == "Pending"
    ).count()
    #Count Pending
    in_progress = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.status == "In Progress"
    ).count()
    #Count Completed
    completed = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.status == "Completed"
    ).count()
    #Return JSON
    return {
        "total_tasks": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed
    }
    
#single obj return    
@task_router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
   # db = SessionLocal()
#SELECT * FROM tasks WHRER id =1 LIMIT=1;
    #task = db.query(Task).filter(Task.id == id).first()

    #db.close()

    return task

#task update
@task_router.put("/tasks/{id}")
def update_task(
    task_id: int, 
    task: TaskCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    #correct task return,only authorized user can update
    db_task = db.query(Task).filter(
    Task.id == task_id,
    Task.owner_id == current_user.id
).first()
   

#to find the record matching id in db
#SELECT * FROM tasks WHERE id = 1 LIMIT 1;
    #existing_task = db.query(Task).filter(Task.id == id).first()
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
    )
    #if existing_task is None:
        #raise HTTPException(
        #status_code=404,
        #detail="Task not found"
        
    db_task.title = task.title
    db_task.priority = task.priority
    db_task.status = task.status
    db_task.deadline = task.deadline

#replacing old values
    #existing_task.title = task.title
    #existing_task.priority = task.priority
    #existing_task.status = task.status

    db.commit()
    db.refresh(db_task)#reloads the object from the database after commit()

    return {
        "message": "Task updated successfully"
}
    
#task delete    
@task_router.delete("/tasks/{id}")
def delete_task(
    task_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
     
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
#find the matching id to delete the record
    #task = db.query(Task).filter(Task.id == id).first()
    #if task is None:
        #raise HTTPException(
           #status_code=404,
            #detail="Task not found"
#delete state mark
    #db.delete(task)
#permenant delete
    db.delete(db_task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }