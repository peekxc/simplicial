import numpy as np 
from typing import * 
from itertools import combinations
from numbers import Integral

# def test_value_type(v: Iterable[Integral]) -> Iterator[Integral]:
#   yield from combinations(v, 2)

#   s = (1,2,3,4,5)
#   test_value_type(s)

# ## so cool: this fails
# s = ('a','b','c','d')
# test_value_type(s)
from splex.meta import * # type: ignore 
from splex.meta import IT
from dataclasses import dataclass

IntType = TypeVar('IntType', int, np.integer, Integral, covariant=True)

@dataclass
class SimplexG(Generic[IntType]):
  vertices: list[IntType]

s = SimplexG([1,2,3])
s = SimplexG([1,2,3])

s = SimplexG([np.int32(1),np.int32(1),np.int32(1)])


def test_generic():
  assert True
