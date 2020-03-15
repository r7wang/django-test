from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.serializers import QuestionSerializer
from mysite.polls.services.question_repo import QuestionRepo


class QuestionSerialization(APIView):
    _question_repo = QuestionRepo()

    def get(self, request):
        questions = self._question_repo.get_all_questions()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)