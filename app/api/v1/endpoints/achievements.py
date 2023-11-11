from uuid import UUID

import aiohttp as aiohttp
from fastapi import Depends, UploadFile
from fastapi.params import File, Form
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.achievements.schema import AchievementShow
from app.achievements.service import AchievementAlreadyExist, Forbidden, AchievementDoesntExist
from app.achievements.service import achievement_service
from app.core.deps import get_db
from app.user.auth.auth import get_current_user_from_token
from app.user.model import User
from app.user.schema import UserShow
from app.user.service import UserDoesntExist

router = APIRouter()


@router.post('/', responses={409: {
    "description": "Achievements already exists error",
    "content": {
        "application/json": {
            "example": AchievementAlreadyExist
        }
    }
}})
async def create_achievements(title: str = Form(...), description: str = File(...), file: UploadFile = File(...),
                              db: AsyncSession = Depends(get_db)
                              ) -> AchievementShow:
    achievement = await achievement_service.create_achievements(title=title, description=description, db=db, file=file)
    return achievement


@router.delete('/', responses={403: {
    "description": "User is not superadmin or admin",
    "content": {
        "application/json": {
            "example": Forbidden
        }
    }
},
    404: {"description": "Achievement doesn't exist",
          "content": {
              "application/json": {
                  "example": AchievementDoesntExist
              },

          }}})
async def delete_achievement(
        id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> AchievementShow:
    deleted_achievement = await achievement_service.delete_achievement(id, db, current_user)
    return deleted_achievement


@router.post("/give_achievement", responses={409: {
    "description": "Achievements already exists error",
    "content": {
        "application/json": {
            "example": AchievementAlreadyExist
        }
    }
},
    404: {"description": "Achievement doesn't exist/ User doesn't exist",
          "content": {
              "Achievement doesn't exist": {
                  "example": AchievementDoesntExist
              },
              "User doesn't exist": {
                  "example": UserDoesntExist
              }

          }}})
async def give_achievement_to_user(user_id: UUID, achievement_id: UUID, db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user_from_token)) -> UserShow:
    return await achievement_service.give_achievement_to_user(user_id=user_id, achievement_id=achievement_id,
                                                              current_user=current_user, db=db)


@router.get('/')
async def get_achievement(id: UUID, db: AsyncSession = Depends(get_db)):
    return await achievement_service.get_achievement(id=id, db=db)


@router.get('/get_file')
async def get_file(id: UUID):
    return await achievement_service.get_file_by_id(id)


@router.post('/send_notification')
async def send_notification(summary: str, content: str, message_id: str, username: str):
    url = 'https://lapsha.vladexa.ru/api/sendNotificationToUser'
    data = {
        'summary': f'{summary}',
        'content': f'{content}',
        'message_id': f'{message_id}',
        'username': f'{username}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return 'Уведомление успешно отправлено'
            else:
                return 'Ошибка при отправке уведомления'
