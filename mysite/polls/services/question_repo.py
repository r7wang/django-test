from datetime import datetime
from typing import Optional, List

from pytz import utc

from mysite.polls.models import Question


class QuestionRepo:
    def get_all_questions(self) -> List[Question]:
        return Question.objects.all()

    def create_question(self, text: str, exc: Optional[Exception] = None) -> Question:
        question = Question(question_text=text, publish_date=datetime.now(tz=utc))
        if exc:
            raise exc
        question.save()
        return question

    def delete_questions(self):
        Question.objects.all().delete()
