from mysite.polls.helpers import math
from mysite.polls.helpers.math import add
from mysite.polls.helpers.math import MathService


class Mocking:
    def run_func_from_module(self, x: int, y: int) -> int:
        return math.add(x, y)

    def run_func_directly(self, x: int, y: int) -> int:
        return add(x, y)

    def run_class_func_from_module(self, x: int, y: int) -> int:
        service = math.MathService()
        return service.add(x, y)

    def run_class_func_from_class(self, x: int, y: int) -> int:
        service = MathService()
        return service.add(x, y)
