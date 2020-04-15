from unittest.mock import MagicMock

from mysite.polls.helpers.math import MathService


class TestPatchObject:
    def test_no_patch(self):
        math_service = MathService()
        result = math_service.add(2, 6)
        assert result == 8

    def test_with_patch(self, mocker):
        math_service = MathService()
        mocker.patch.object(math_service, 'add', MagicMock(return_value=3))
        result = math_service.add(2, 6)
        assert result == 3

    def test_with_patch_multiple_objects(self, mocker):
        math_service_a = MathService()
        math_service_b = MathService()
        mocker.patch.object(math_service_a, 'add', MagicMock(return_value=3))

        result_a = math_service_a.add(2, 6)
        result_b = math_service_b.add(2, 6)
        assert result_a == 3
        assert result_b == 8

    def test_with_patch_class(self, mocker):
        math_service_a = MathService()
        math_service_b = MathService()
        # Patch first or later doesn't even matter.
        mocker.patch.object(MathService, 'add', MagicMock(return_value=3))

        result_a = math_service_a.add(2, 6)
        result_b = math_service_b.add(6, 12)
        assert result_a == 3
        assert result_b == 3
