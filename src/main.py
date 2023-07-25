from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from .adapters import rabbit, redis
from .core.config import settings


def prepare_app(routers: tuple[APIRouter]) -> FastAPI:
    app_ = FastAPI(
        title=settings.project_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app_.include_router(router)
    return app_


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    rabbit.rabbit = rabbit.RMQ()
    await rabbit.rabbit.connect(settings.get_amqp_uri())


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await rabbit.rabbit.close()
