from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.scheduler import task


app_scheduler: AsyncIOScheduler | None = None


async def get_scheduler() -> AsyncIOScheduler:
    return app_scheduler
