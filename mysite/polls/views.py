import json
from datetime import datetime
from typing import Optional

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.polls.exceptions import GenericException
from mysite.polls.serializers import QuestionSerializer, ChoiceSerializer
from mysite.polls.models import Question, Choice
from mysite.polls.services.choices_repo import ChoicesRepo


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


def delete_choices():
    Choice.objects.all().delete()


def delete_questions():
    Question.objects.all().delete()


def make_choice(question: Question, text: str) -> Choice:
    choice = Choice(question=question, choice_text=text, publish_date=datetime.now(tz=utc))
    choice.save()
    return choice


def make_question(text: str, exc: Optional[Exception] = None) -> Question:
    question = Question(question_text=text, publish_date=datetime.now(tz=utc))
    if exc:
        raise exc
    question.save()
    return question


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


class RelatedView(APIView):
    _choices_repo = ChoicesRepo()

    def get(self, request):
        delete_choices()
        delete_questions()

        question = make_question('Question A')
        make_choice(question, 'Choice A')
        make_choice(question, 'Choice B')

        choices = self._choices_repo.get_question_choices(question)

        data = {}
        for choice in choices:
            data[choice.id] = choice.choice_text
        return Response(data=data)


class NoTransaction(APIView):
    def get(self, request, *args, **kwargs):
        # Writes objects to the database but throws an exception before the entire operation completes; does not use
        # any save points.
        delete_questions()

        try:
            make_question('Question A')
            make_question('Question B', GenericException())
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text
        return Response(data=data)


class WithTransaction(APIView):
    def get(self, request, *args, **kwargs):
        delete_questions()

        try:
            with transaction.atomic():
                make_question('Question A')
                make_question('Question B', GenericException())
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text
        return Response(data=data)


class NestedTransaction(APIView):
    def get(self, request, *args, **kwargs):
        delete_questions()

        try:
            with transaction.atomic():
                make_question('Question A')

                # Higher-level API used to partially rollback a transaction.
                try:
                    with transaction.atomic():
                        make_question('Question B')
                        make_question('Question C', GenericException())
                except GenericException:
                    pass
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text
        return Response(data=data)


class NestedSavePoint(APIView):
    def get(self, request, *args, **kwargs):
        Question.objects.all().delete()

        try:
            with transaction.atomic():
                make_question('Question A')

                # Lower-level API used to partially rollback a transaction.
                sid = transaction.savepoint()
                try:
                    make_question('Question B')
                    make_question('Question C', GenericException())
                except GenericException:
                    make_question('Question D')
                    transaction.savepoint_rollback(sid)
                else:
                    transaction.savepoint_commit(sid)
        except GenericException:
            pass

        data = {}
        questions = Question.objects.all()
        for question in questions:
            data[question.id] = question.question_text

        return Response(data=data)
