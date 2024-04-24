from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas import STaskAdd, STask, STaskId

from repository import TaskRepository

router = APIRouter(prefix="/tasks",
                   tags=["Задачи"])


@router.post("")
async def create_task(
        task: Annotated[STaskAdd, Depends()],
        session: AsyncSession = Depends(get_session)
) -> STaskId:

    task_id = await TaskRepository.add_one(data=task,
                                           session=session)
    return {"ok": True, "id": task_id}


@router.get("")
async def root(session: AsyncSession = Depends(get_session)) -> list[STask]:

    tasks = await TaskRepository.get_all(session=session)
    return tasks
