from adapters import rabbit, redis, postgres
from redis.asyncio import Redis
from core.config import settings
from services.scheduler import scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def startup() -> None:
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    rabbit.rabbit = rabbit.RMQ()
    await rabbit.rabbit.connect(
        url=settings.get_amqp_uri()
    )
    scheduler.app_scheduler = AsyncIOScheduler()


async def shutdown() -> None:
    if redis.redis is not None:
        await redis.redis.close()

    if rabbit.rabbit is not None:
        await rabbit.rabbit.close()

