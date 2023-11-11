import uuid
from pathlib import Path
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.params import File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app.achievements.schema import AchievementBase, AchievementShow
from app.achievements.schema import AchievementCreate
from app.core import store
from app.core.deps import get_db
from app.user.auth.auth import get_current_user_from_token
from app.user.model import User
from app.user.service import UserDoesntExist

# from utils.security import create_access_token


AchievementDoesntExist = HTTPException(
    status_code=404, detail=f"Achievement with this id not found."
)
AchievementAlreadyExist = HTTPException(status_code=409, detail="Achievement already exists")

Forbidden = HTTPException(status_code=403, detail="forbidden.")

IMAGEDIR = 'images/'


class AchievementService:
    async def create_achievements(self, title: str, description: str, db: AsyncSession = Depends(get_db),
                                  file: UploadFile = File(...)) -> AchievementBase:
        achievement = await store.achievements.get_by_title(title, db)
        if achievement:
            raise AchievementAlreadyExist
        file_id = uuid.uuid4()
        file.filename = f"{file_id}.jpg"
        contents = await file.read()
        path = f'{IMAGEDIR}{file.filename}'
        filepath = Path(IMAGEDIR)
        filepath.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(contents)
        achievement = await store.achievements.create(
            db,
            obj_in=AchievementCreate(
                title=title,
                description=description,
                image=str(file_id)
            )
        )
        return achievement

    async def delete_achievement(self,
                                 id: UUID,
                                 db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(get_current_user_from_token),
                                 ) -> AchievementShow:
        if not self.__check_user_permissions(current_user=current_user):
            raise Forbidden
        achievement_for_deletion = await store.achievements.get(db, id)
        if achievement_for_deletion is None:
            raise AchievementDoesntExist
        deleted_achievement_id = await store.achievements.remove(db=db, id=id)
        if deleted_achievement_id is None:
            raise HTTPException(
                status_code=404, detail=f"Achievement with id {deleted_achievement_id} not found."
            )
        return deleted_achievement_id

    def __check_user_permissions(self, current_user: User) -> bool:
        if current_user.is_superadmin or current_user.is_admin:
            return True

    async def give_achievement_to_user(self, user_id: UUID, achievement_id: UUID, db: AsyncSession, current_user: User):
        user = await store.user.get(user_id=user_id, db=db)
        if not user:
            raise UserDoesntExist
        if not self.__check_user_permissions(current_user=current_user):
            raise Forbidden
        achievement = await store.achievements.get(id=achievement_id, db=db)
        if achievement in user.achievements:
            raise AchievementAlreadyExist
        if not achievement:
            raise AchievementDoesntExist
        user.achievements.append(achievement)
        await db.commit()
        return user

    async def upload_image(self, file: UploadFile = File(...)):
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
        path = f'{IMAGEDIR}{file.filename}'
        filepath = Path(IMAGEDIR)
        filepath.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(contents)
        return file.filename

    async def get_file_by_id(self, id):
        try:
            path = f'{IMAGEDIR}{id}.jpg'
        except FileNotFoundError:
            raise HTTPException(400, detail='File not found!')

        return FileResponse(path)

    async def get_achievement(self, id: UUID, db: AsyncSession):
        return await store.achievements.get(db=db, id=id)


achievement_service = AchievementService()

#
#
# async def get_user(
#         db: AsyncSession = Depends(get_db),
#         current_user: User = Depends(get_current_user_from_token),
# ):
#     return await store.user.get(db, current_user.user_id)
