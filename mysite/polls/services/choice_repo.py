from datetime import datetime
from typing import List

from pytz import utc

from mysite.polls.models import Choice, Question


class ChoiceRepo:
    def get_question_choices(self, question: Question) -> List[Choice]:
        return [choice for choice in question.choices.all()]

    def delete_choices(self):
        Choice.objects.all().delete()

    def create_choice(self, question: Question, text: str) -> Choice:
        choice = Choice(question=question, choice_text=text, publish_date=datetime.now(tz=utc))
        choice.save()
        return choice
