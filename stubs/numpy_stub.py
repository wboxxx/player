import random as _random
import builtins

__all__ = [
    'array', 'arange', 'asarray', 'max', 'mean', 'std', 'zeros_like',
    'diff', 'abs', 'where', 'random', 'testing', 'float32', 'ndarray'
]


class ndarray(list):
    pass

float32 = float


def array(obj):
    if isinstance(obj, list):
        return ndarray(obj)
    try:
        return ndarray(list(obj))
    except TypeError:
        return ndarray([obj])


def asarray(obj):
    return array(obj)

def arange(n):
    return list(range(int(n)))

def max(seq):
    return builtins.max(seq)

def mean(seq):
    return sum(seq) / len(seq) if seq else 0.0

def std(seq):
    if not seq:
        return 0.0
    m = mean(seq)
    return (sum((x - m) ** 2 for x in seq) / len(seq)) ** 0.5

def zeros_like(seq):
    return [0 for _ in seq]

def diff(seq):
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]

def abs(x):
    if isinstance(x, list):
        return [builtins.abs(v) for v in x]
    return builtins.abs(x)

def where(condition):
    return ([i for i, v in enumerate(condition) if v],)

class RandomModule:
    def rand(self, n):
        return [_random.random() for _ in range(int(n))]

random = RandomModule()

class TestingModule:
    @staticmethod
    def assert_array_equal(a, b):
        assert list(a) == list(b), f'{a} != {b}'

class testing:
    assert_array_equal = staticmethod(TestingModule.assert_array_equal)

