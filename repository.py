from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import TaskOrm
from schemas import STaskAdd, STask


class TaskRepository:

    @classmethod
    async def add_one(cls, data: STaskAdd, session: AsyncSession):

        task_dict = data.model_dump()
        task = TaskOrm(**task_dict)
        session.add(task)
        await session.flush()
        await session.commit()
        return task.id

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[STask]:

        query = select(TaskOrm)
        result = await session.execute(query)
        task_models = result.scalars().all()
        task_schemas = [STask.validate(task_model) for task_model in task_models]
        return task_schemas
