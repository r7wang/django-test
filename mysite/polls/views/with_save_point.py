from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.exceptions import GenericException
from mysite.polls.services.question_repo import QuestionRepo


@method_decorator(transaction.non_atomic_requests, 'dispatch')
class WithSavePoint(APIView):
    """
    When you only use save points, it's as if you didn't use save points at all. If it were to act like a transaction,
    on failure to create Question B, we would've also rolled back the creation of Question A. Instead we see Question A
    in the results.
    """

    _question_repo = QuestionRepo()

    def get(self, request):
        self._question_repo.delete_questions()

        sid = transaction.savepoint()
        try:
            self._question_repo.create_question('Question A')
            self._question_repo.create_question('Question B', GenericException())
        except GenericException:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

        data = {}
        questions = self._question_repo.get_all_questions()
        for question in questions:
            data[question.pk] = question.question_text
        return Response(data=data)
