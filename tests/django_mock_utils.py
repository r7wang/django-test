from typing import Type

from django_mock_queries.query import MockSet


def mock_django_model(mocker, model_type: Type) -> MockSet:
    mock_set = MockSet(model=model_type)
    mocker.patch.object(model_type, 'objects', mock_set)
    return mock_set
