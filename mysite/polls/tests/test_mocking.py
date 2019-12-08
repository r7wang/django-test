from unittest.mock import MagicMock

import pytest

from mysite.polls.services.mocking import Mocking


@pytest.fixture
def mocking_obj():
    return Mocking()


@pytest.fixture
def math_module_mock(mocker):
    def _math_module_mock(is_global: bool):
        module = MagicMock()
        if is_global:
            mocker.patch('mysite.polls.helpers.math', module)
        else:
            mocker.patch('mysite.polls.services.mocking.math', module)
        return module
    return _math_module_mock


@pytest.fixture
def math_func_mock(mocker):
    def _math_func_mock(is_global: bool, val: int):
        func = MagicMock(return_value=val)
        if is_global:
            mocker.patch('mysite.polls.helpers.math.add', func)
        else:
            mocker.patch('mysite.polls.services.mocking.add', func)
        return func
    return _math_func_mock

@pytest.fixture
def math_class_mock(mocker):
    def _math_class_mock(is_global: bool, val: int):
        cls = MagicMock()
        func = MagicMock(return_value=val)
        mocker.patch.object(cls, 'add', func)
        if is_global:
            mocker.patch('mysite.polls.helpers.math.MathService', MagicMock(return_value=cls))
        else:
            mocker.patch('mysite.polls.services.mocking.MathService', MagicMock(return_value=cls))
        return cls
    return _math_class_mock


class TestRunFuncFromModule:
    """
    Tests functions defined directly on modules where module is imported.
    """

    def test_mock_global_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the global math module.
         - Module is locally imported; mocks have no effect.
        """
        module = math_module_mock(is_global=True)
        func_mock = MagicMock(return_value=3)
        mocker.patch.object(module, 'add', func_mock)
        val = mocking_obj.run_func_from_module(2, 6)
        assert val == 8

    def test_mock_local_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the math module local to Mocking service.
         - Module is locally imported; mocks take effect.
        """
        module = math_module_mock(is_global=False)
        func_mock = MagicMock(return_value=3)
        mocker.patch.object(module, 'add', func_mock)
        val = mocking_obj.run_func_from_module(2, 6)
        assert val == 3

    def test_mock_global_func(self, mocking_obj, math_func_mock):
        """
         - Mock out the global add function.
         - Module is not mocked, but global module function is still used because it wasn't imported.
        """
        func = math_func_mock(is_global=True, val=3)
        val = mocking_obj.run_func_from_module(2, 6)
        assert val == 3

    def test_mock_local_func(self, mocking_obj, math_func_mock):
        """
         - Mock out add function local to Mocking service.
         - Function is not locally imported; mocks have no effect.
        """
        func = math_func_mock(is_global=False, val=3)
        val = mocking_obj.run_func_from_module(2, 6)
        assert val == 8


class TestRunFuncDirectly:
    """
    Tests functions defined directly on modules where function is imported.
    """

    def test_mock_global_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the global math module.
         - Module is not locally imported; mocks STILL have no effect (why?).
        """
        module = math_module_mock(is_global=True)
        func_mock = MagicMock(return_value=3)
        mocker.patch.object(module, 'add', func_mock)
        val = mocking_obj.run_func_directly(2, 6)
        assert val == 8

    def test_mock_local_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the math module local to Mocking service.
         - Module is not locally imported; mocks have no effect.
        """
        module = math_module_mock(is_global=False)
        func_mock = MagicMock(return_value=3)
        mocker.patch.object(module, 'add', func_mock)
        val = mocking_obj.run_func_directly(2, 6)
        assert val == 8

    def test_mock_global_func(self, mocking_obj, math_func_mock):
        """
         - Mock out the global add function.
         - Mocking resolves add in a different way; mocks have no effect.
        """
        func = math_func_mock(is_global=True, val=3)
        val = mocking_obj.run_func_directly(2, 6)
        assert val == 8

    def test_mock_local_func(self, mocking_obj, math_func_mock):
        """
         - Mock out the global add function.
         - Function is directly imported into local scope; mocks take effect.
        """
        func = math_func_mock(is_global=False, val=3)
        val = mocking_obj.run_func_directly(2, 6)
        assert val == 3


class TestRunClassFuncFromModule:
    """
    Tests class functions defined on modules where module is imported.
    """

    def test_mock_global_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the global math module.
         - Module is locally imported; mocks have no effect.
        """
        module = math_module_mock(is_global=True)
        func_mock = MagicMock(return_value=3)
        class_mock = MagicMock()
        mocker.patch.object(module, 'MathService', class_mock)
        mocker.patch.object(class_mock, 'add', func_mock)
        val = mocking_obj.run_class_func_from_module(2, 6)
        assert val == 8

    def test_mock_local_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the math module local to Mocking service.
         - Seems like you can't chain mock from module to class.
        """
        module = math_module_mock(is_global=False)
        func_mock = MagicMock(return_value=3)
        class_mock = MagicMock()
        mocker.patch.object(module, 'MathService', class_mock)
        mocker.patch.object(class_mock, 'add', func_mock)
        val = mocking_obj.run_class_func_from_module(2, 6)
        assert isinstance(val, MagicMock)

    def test_mock_global_class(self, mocker, mocking_obj, math_class_mock):
        """
         - Mock out the global MathService class.
         - Module is not mocked, but global module class is still used because it wasn't imported.
        """
        cls = math_class_mock(is_global=True, val=3)
        val = mocking_obj.run_class_func_from_module(2, 6)
        assert val == 3

    def test_mock_local_class(self, mocker, mocking_obj, math_class_mock):
        """
         - Mock out MathService class local to Mocking service.
         - Class is not locally imported; mocks have no effect.
        """
        cls = math_class_mock(is_global=False, val=3)
        val = mocking_obj.run_class_func_from_module(2, 6)
        assert val == 8


class TestRunClassFuncFromClass:
    """
    Tests class functions defined on modules where class is imported.
    """

    def test_mock_global_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the global math module.
         - Module is not locally imported; mocks STILL have no effect (why?).
        """
        module = math_module_mock(is_global=True)
        func_mock = MagicMock(return_value=3)
        class_mock = MagicMock()
        mocker.patch.object(module, 'MathService', class_mock)
        mocker.patch.object(class_mock, 'add', func_mock)
        val = mocking_obj.run_class_func_from_class(2, 6)
        assert val == 8

    def test_mock_local_module(self, mocker, mocking_obj, math_module_mock):
        """
         - Mock out the math module local to Mocking service.
         - Module is not locally imported; mocks have no effect.
        """
        module = math_module_mock(is_global=False)
        func_mock = MagicMock(return_value=3)
        class_mock = MagicMock()
        mocker.patch.object(module, 'MathService', class_mock)
        mocker.patch.object(class_mock, 'add', func_mock)
        val = mocking_obj.run_class_func_from_class(2, 6)
        assert val == 8

    def test_mock_global_class(self, mocker, mocking_obj, math_class_mock):
        """
         - Mock out the global MathService class.
         - Mocking resolves MathService in a different way; mocks have no effect.
        """
        cls = math_class_mock(is_global=True, val=3)
        val = mocking_obj.run_class_func_from_class(2, 6)
        assert val == 8

    def test_mock_local_class(self, mocker, mocking_obj, math_class_mock):
        """
         - Mock out MathService class local to Mocking service.
         - Class is directly imported into local scope; mocks take effect.
        """
        cls = math_class_mock(is_global=False, val=3)
        val = mocking_obj.run_class_func_from_class(2, 6)
        assert val == 3
