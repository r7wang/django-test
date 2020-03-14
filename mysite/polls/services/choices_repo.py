from typing import List

from mysite.polls.models import Choice, Question


class ChoicesRepo:
    def get_question_choices(self, question: Question) -> List[Choice]:
        return [question.choices]
