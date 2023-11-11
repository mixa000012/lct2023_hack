import json

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI
from app.core import store
from app.core.config import settings
from app.core.deps import get_db
from app.questions.schema import QuestionCreate, GenerateQuiz
from app.user.model import User


class SurveyDoesntExist(Exception):
    pass


async def create_question(obj: QuestionCreate, current_user: User, db: AsyncSession = Depends(get_db)):
    survey = await store.survey.get(id=obj.article_id, db=db)
    if survey:
        question = await store.question.create_question(db=db, obj_in=obj, user_id=current_user.user_id)
    else:
        raise SurveyDoesntExist
    return question


async def get_question(db: AsyncSession = Depends(get_db)):
    question = await store.question.get_question_with_options(db=db, skip=0, limit=100)
    return question


def generate_quiz(obj: GenerateQuiz):
    client = OpenAI(api_key=f"{settings.API_KEY}")
    context = "Use the following step-by-step instructions to generate a JSON-formatted quiz for an article in its original language.\n1. The user will provide you with text from an article. Summarize the text, focusing on essential points or key arguments.\n2. Using the summary, create 8 multiple-choise questions for the quiz that covers significant aspects of the content. The quiz has to be written in the original language of the text.\n3. Ensure that each question has 3-5 possible answers that are not repeated and only one answer is correct according to the summary but isn't too obvious.\n4. Provide output only in JSON format as follows. Do not write anything except JSON in responce.\n{\n\"questions\": [list of string questions],\n\"possible_answers\": [[list of string possible answers for question1], [list of string possible answers for question2], ...],\n\"correct_answers\": [list of indexes of the correct answers for questions]\n}"
    messages = [{"role": "system", "content": context}, {"role": "user", "content": obj.article_text}]

    chat_completion = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo-1106",
                                                     response_format={"type": "json_object"})
    response = chat_completion.choices[0].message.content
    response = json.loads(response)
    if (chat_completion.choices[0].finish_reason == "length"):
        return ""
    else:
        return response


class QuestionDoenstExist(Exception):
    pass
