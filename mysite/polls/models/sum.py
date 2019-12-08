from typing import List


class Sum:
    def __init__(self, val: int):
        self.val = val

    @classmethod
    def objects(cls) -> List:
        return [
            Sum(1),
            Sum(3),
            Sum(5),
            Sum(8),
        ]
