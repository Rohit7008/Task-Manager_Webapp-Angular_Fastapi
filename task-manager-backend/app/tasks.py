# app/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List
from .models import Task, TaskCreate, TaskRead
from .database import get_session
from .deps import get_current_user
from sqlmodel import Session

router = APIRouter()

@router.post("/", response_model=TaskRead)
def create_task(task_in: TaskCreate, user=Depends(get_current_user), session=Depends(get_session)):
    task = Task.from_orm(task_in)
    task.owner_id = user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/", response_model=List[TaskRead])
def read_tasks(user=Depends(get_current_user), session=Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.owner_id == user.id)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_in: TaskCreate, user=Depends(get_current_user), session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_in.title
    task.description = task_in.description
    task.completed = task_in.completed
    task.due_date = task_in.due_date
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
