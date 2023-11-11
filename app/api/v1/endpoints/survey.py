import uuid
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.user.auth.auth import get_current_user_from_token, get_device_id_from_token
from app.article import service
from app.user.model import User
from app.article.schema import ArticleCreate, ArticleBase, ArticleShow, Deadline

router = APIRouter()


@router.post('/')
async def create_article(obj: ArticleCreate, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    answer = await service.create_arcticle(db=db, obj_in=obj, current_user=current_user)
    return answer


@router.get('/')
async def get_questions(id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> ArticleShow:
    answers = await service.get_questions(id=id, db=db)
    return answers


@router.get('/deadlines')
async def get_deadlines_from_user(db: AsyncSession = Depends(get_db),
                                  current_user: User = Depends(get_current_user_from_token)) -> List[Deadline]:
    return await service.get_deadlines_from_user(current_user, db)


@router.get('/deadline')
async def get_deadline(survey_ud: uuid.UUID, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)) -> List[Deadline]:
    return await service.get_deadlines_from_user(current_user, db)
