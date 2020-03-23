from django.db.models import ManyToOneRel
from django_mock_queries.query import MockSet

from mysite.polls.models import Choice, Question
from mysite.polls.services.choice_repo import ChoiceRepo
from tests.django_mock_utils import mock_django_model


class TestGetQuestionChoices:
    def _mock_reverse_many_to_one(self, mocker, result: MockSet):
        # NOTE: This approach mocks the creation of reverse many-to-one managers. We can't do an assignment directly
        #       to the reverse side of a related set. The downside is that without additional processing, all reverse
        #       many-to-one managers will be mocked to return the same result. See sample code below.
        #
        # mgr = mocker.MagicMock()
        # factory_orig = related_descriptors.create_reverse_many_to_one_manager
        #
        # def mgr_factory(superclass, rel):
        #     if rel.model == User and rel.name == 'auth_token_set':
        #         return mgr
        #     else:
        #         return factory_orig(superclass, rel)
        #
        # mocker.patch(
        #     'django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager',
        #     mgr_factory
        # )

        def mgr_factory(superclass: type, relation: ManyToOneRel):
            # Depending on the related_name, we may want to return something different here. That should allow us to
            # build a library for mocking that might look something like this:
            #   - Given (relation.related_name='choices', relation.model=Question), return ...
            # return mocker.MagicMock(return_value=mgr)

            # We are mocking that all x.related returns result. This is insufficient if x can be a range of model
            # instances which have different relations. In that case, we probably have to do a relationship check and
            # find the related objects for each case.
            return mocker.MagicMock(return_value=result)

            # We need the following arguments:
            #   - model type (Question)
            #   - related name ('choices')
            #
            # What we can do is say that if our model type and related name, then mgr_factory returns the mock.
            # Otherwise, it just returns the factory_orig(superclass, rel).

        mocker.patch(
            'django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager',
            mgr_factory,
        )

    def test_expect_related_name_when_query(self, mocker):
        choices = mock_django_model(mocker, model_type=Choice)

        q1 = Question(pk=1, question_text='Test Question?')
        c1 = Choice(pk=1, question=q1, choice_text='Choice A')
        choices.add(c1)

        self._mock_reverse_many_to_one(mocker, choices)

        repo = ChoiceRepo()
        result = repo.get_question_choices(q1)
        assert result == [c1]
        del Question.choices.related_manager_cls

    def test_expect_related_name_when_query_startswith(self, mocker):
        choices = mock_django_model(mocker, model_type=Choice)

        q1 = Question(pk=1, question_text='How do you feel?')
        c1 = Choice(pk=1, question=q1, choice_text='Good: excellent!')
        c2 = Choice(pk=2, question=q1, choice_text='Good: awesome!')
        c3 = Choice(pk=3, question=q1, choice_text='Bad: sick...')
        choices.add(c1, c2, c3)

        self._mock_reverse_many_to_one(mocker, choices)

        repo = ChoiceRepo()
        result = repo.get_question_choices_starting_with(q1, 'Bad')
        assert result == [c3]
        del Question.choices.related_manager_cls
