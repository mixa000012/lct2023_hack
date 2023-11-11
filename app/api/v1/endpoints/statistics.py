from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.statistics import service
from app.statistics.schema import StatisticsCreate
from app.questions.service import SurveyDoesntExist
from app.user.auth.auth import get_current_user_from_token
from app.user.model import User

router = APIRouter()


@router.post('/')
async def create_statistics(obj: StatisticsCreate, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user_from_token)):
    return await service.create_statistics(db=db, obj=obj, current_user=current_user)


@router.get('/')
async def get_statistic(db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    return await service.get_statistic(db=db, current_user=current_user)


@router.get('/article')
async def get_statistic_by_article(article_id: UUID, db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user_from_token)):
    return await service.get_statistic_by_article(db=db, current_user=current_user, article_id=article_id)
