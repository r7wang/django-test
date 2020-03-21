from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.exceptions import GenericException
from mysite.polls.services.question_repo import QuestionRepo


class WithTransaction(APIView):
    """
    When you use a transaction, on failure to create Question B, we will also rollback Question A.
    """

    _question_repo = QuestionRepo()

    def get(self, request):
        self._question_repo.delete_questions()

        try:
            with transaction.atomic():
                self._question_repo.create_question('Question A')
                self._question_repo.create_question('Question B', GenericException())
        except GenericException:
            pass

        data = {}
        questions = self._question_repo.get_all_questions()
        for question in questions:
            data[question.pk] = question.question_text
        return Response(data=data)