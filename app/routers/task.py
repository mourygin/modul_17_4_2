from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task
from models import User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    # task = db.scalars(select(Task).where(Task.id == task_id)).all()
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The task not found.'
        )
    return task

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):

    # Выясняем существует ли указанный пользователь
    user = db.scalar(select(User).where(User.id == user_id, User.active == 1))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user not found.'
        )

    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   completed=False,
                                   user_id=create_task.user_id,
                                   slug=slugify(create_task.title),
                                   active=1))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    # task = db.scalars(select(Task).where(Task.id == task_id))
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The task not found.'
        )
    db.execute(update(Task).where(Task.id == task_id).values(
        title = update_task.title,
        content = update_task.content,
        priority = update_task.priority,
        completed = update_task.completed,
        user_id = update_task.user_id,
        active = update_task.active
    ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'The user has been updated successful.'
    }

@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The task not found.'
        )
    db.execute(update(Task).where(Task.id == task_id).values(active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'The task has been deleted successful.'
    }