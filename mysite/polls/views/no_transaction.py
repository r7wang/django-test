from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.exceptions import GenericException
from mysite.polls.services.question_repo import QuestionRepo


class NoTransaction(APIView):
    _question_repo = QuestionRepo()

    def get(self, request):
        # Writes objects to the database but throws an exception before the entire operation completes; does not use
        # any save points.
        self._question_repo.delete_questions()

        try:
            self._question_repo.create_question('Question A')
            self._question_repo.create_question('Question B', GenericException())
        except GenericException:
            pass

        data = {}
        questions = self._question_repo.get_all_questions()
        for question in questions:
            data[question.pk] = question.question_text
        return Response(data=data)
