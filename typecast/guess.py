from collections import defaultdict

from typecast.value import String, Integer, Decimal, Boolean
from typecast.date import Date, DateTime

GUESS_TYPES = [String, Decimal, Integer, Boolean, Date, DateTime]
FAILED = 'failed'


class TypeGuesser(object):
    """Guess the best matching type for a series of values."""

    default = String()

    def __init__(self, types=GUESS_TYPES, strict=False):
        self.scores = defaultdict(int)
        self.instances = [i for t in types for i in t.instances()]
        self.strict = strict

    def add(self, value):
        if self.default._is_null(value):
            return
        classes = {}
        for inst in self.instances:
            cls = type(inst)
            if cls not in classes:
                classes[cls] = inst.test_class(value)
            if self.scores[inst] is FAILED or not classes[cls]:
                continue

            result = inst.test(value)
            if self.strict and (result == -1):
                if not isinstance(inst, String):
                    self.scores[inst] = FAILED
            elif result == 1:
                self.scores[inst] += inst.guess_score

    @property
    def best(self):
        best_score = 0
        best_inst = self.default
        for inst in self.instances:
            score = self.scores.get(inst, 0)
            if score is not FAILED and score > best_score:
                best_score = score
                best_inst = inst
        return best_inst
