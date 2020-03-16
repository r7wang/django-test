import json

from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.serializers import ChoiceSerializer


class ChoiceSerialization(APIView):
    def get(self, request):
        json_str = '{' \
               '"question_id": 1,' \
               '"choice_text": "Another choice...",' \
               '}'
        data = json.loads(json_str)
        serializer = ChoiceSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        return Response(valid_data)
