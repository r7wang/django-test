from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.services.choice_repo import ChoiceRepo
from mysite.polls.services.question_repo import QuestionRepo


class RelatedName(APIView):
    _choice_repo = ChoiceRepo()
    _question_repo = QuestionRepo()

    def get(self, request):
        self._choice_repo.delete_choices()
        self._question_repo.delete_questions()

        question = self._question_repo.create_question('Question A')
        self._choice_repo.create_choice(question, 'Choice A')
        self._choice_repo.create_choice(question, 'Choice B')

        choices = self._choice_repo.get_question_choices(question)

        data = {}
        for choice in choices:
            data[choice.pk] = choice.choice_text
        return Response(data=data)
