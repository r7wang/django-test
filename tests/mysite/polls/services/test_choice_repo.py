from typing import List

import pytest
from django.db.models import ManyToOneRel
from django_mock_queries.query import MockSet

from mysite.polls.models import Choice, Question
from mysite.polls.services.choice_repo import ChoiceRepo


class TestGetQuestionChoices:
    def _mock_reverse_many_to_one(self, mocker, result: List):
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

        # This will only work for `all` but we may also want to handle common cases such as `filter`.
        mgr = mocker.MagicMock()
        mocker.patch.object(mgr, 'all', return_value=result)

        def mgr_factory(superclass: type, relation: ManyToOneRel):
            # Depending on the related_name, we may want to return something different here. That should allow us to
            # build a library for mocking that might look something like this:
            #   - Given (relation.related_name='choices', relation.model=Question), return ...
            return mocker.MagicMock(return_value=mgr)

        mocker.patch(
            'django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager',
            mgr_factory,
        )

    @pytest.mark.django_db
    def test_expect_related_name_when_query(self, mocker):
        questions = MockSet(model=Question)
        mocker.patch.object(Question, 'objects', questions)

        choices = MockSet(model=Choice)
        mocker.patch.object(Choice, 'objects', choices)

        q1 = Question(pk=1, question_text='Test Question?')
        questions.add(q1)

        c1 = Choice(pk=1, choice_text='Choice A', question=q1)
        choices.add(c1)

        self._mock_reverse_many_to_one(mocker, [c1])

        repo = ChoiceRepo()
        choices = repo.get_question_choices(q1)
        assert choices == [c1]
