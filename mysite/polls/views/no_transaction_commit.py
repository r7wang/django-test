from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.services.question_repo import QuestionRepo


@method_decorator(transaction.non_atomic_requests, 'dispatch')
class NoTransactionCommit(APIView):
    """
    When you only use save points, it's as if you didn't use save points at all. If it were to act like a transaction,
    on failure to create Question B, we would've also rolled back the creation of Question A. Instead we see Question A
    in the results.
    """

    _question_repo = QuestionRepo()

    def get(self, request):
        self._question_repo.delete_questions()

        transaction.on_commit(
            lambda: self._question_repo.delete_questions()
        )
        return Response()
