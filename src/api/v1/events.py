from fastapi import APIRouter, Depends
from fastapi import Body
from models.notifications import NewSeriesModel, VerifyUserModel, LikeModel
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.postgres import get_session
from services.notifications import get_notifications_service, FastNotificationsService

router = APIRouter()


@router.post(
    '/new_series',
    description='Метод создает уведомление о новой серии',
)
async def create_new_series_notification(
    series: NewSeriesModel = Body(),
    session: AsyncSession = Depends(get_session),
    service: FastNotificationsService = Depends(get_notifications_service),
) -> None:

    await service.check_new_series(
        session=session,
        new_series=series,
    )


@router.post(
    '/verify',
    description='Метод создает уведомление о подтверждении регистрации',
)
async def create_event_verify(
    verify_user: VerifyUserModel,
    service: FastNotificationsService = Depends(get_notifications_service),
) -> None:

    await service.verify_email(
        new_verify=verify_user,
    )


@router.post(
    '/new_like',
    description='Метод создает уведомление о новых лайках',
)
async def create_likes_notification(
    like: LikeModel = Body(),
    service: FastNotificationsService = Depends(get_notifications_service),
) -> None:

    await service.like_event(
        new_like=like,
    )
