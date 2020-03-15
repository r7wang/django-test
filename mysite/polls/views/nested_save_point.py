from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.exceptions import GenericException
from mysite.polls.services.question_repo import QuestionRepo


class NestedSavePoint(APIView):
    _question_repo = QuestionRepo()

    def get(self, request):
        self._question_repo.delete_questions()

        try:
            with transaction.atomic():
                self._question_repo.create_question('Question A')

                # Lower-level API used to partially rollback a transaction.
                sid = transaction.savepoint()
                try:
                    self._question_repo.create_question('Question B')
                    self._question_repo.create_question('Question C', GenericException())
                except GenericException:
                    self._question_repo.create_question('Question D')
                    transaction.savepoint_rollback(sid)
                else:
                    transaction.savepoint_commit(sid)
        except GenericException:
            pass

        data = {}
        questions = self._question_repo.get_all_questions()
        for question in questions:
            data[question.pk] = question.question_text
        return Response(data=data)
