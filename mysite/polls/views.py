import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import GenericException
from .serializers import QuestionSerializer, ChoiceSerializer
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


class QuestionView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class ChoiceView(APIView):
    def get(self, request):
        json_str = '{' \
               '"question_id": 1,' \
               '"choice_text": "Another choice...",' \
               '"publish_date": "2019-10-25T08:30"' \
               '}'
        data = json.loads(json_str)
        serializer = ChoiceSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        return Response(valid_data)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class NoSavePoint(APIView):
    def get(self, request, *args, **kwargs):
        # Writes objects to the database but throws an exception before the entire operation completes; does not use
        # any save points.
        Question.objects.all().delete()

        try:
            question_a = Question(question_text='Question A', publish_date=datetime.now())
            question_a.save()

            question_b = Question(question_text='Question B', publish_date=datetime.now())
            raise GenericException()
            question_b.save()
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text

        return Response(data=data)


class WithSavePoint(APIView):
    def get(self, request, *args, **kwargs):
        Question.objects.all().delete()

        try:
            with transaction.atomic():
                question_a = Question(question_text='Question A', publish_date=datetime.now())
                question_a.save()

                question_b = Question(question_text='Question B', publish_date=datetime.now())
                raise GenericException()
                question_b.save()
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text

        return Response(data=data)
