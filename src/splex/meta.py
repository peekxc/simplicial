## meta.py
## Contains definitions and utilities for prescribing a structural type system on the 
## space of abstract simplicial complexes and on simplicial filtrations
from __future__ import annotations
from abc import abstractmethod
from typing import *
from itertools import *
from functools import total_ordering
from numbers import Number, Integral
from numpy.typing import ArrayLike
from collections.abc import Hashable

import numpy as np 

# IT = TypeVar('IT', bound=Union[int, np.integer, Integral])
IT = TypeVar('IT', int, np.integer, Integral, covariant=True)


# Based on https://www.timekl.com/blog/2014/12/14/learning-swift-convertibles/
@runtime_checkable
class SimplexConvertible(Collection, Protocol[IT]):
  """Protocol class for simplex-convertible types. 
  
  Any collection of integer-like values is convertible to a Simplex type.
  """
  pass

# @runtime_checkable
# class PropertySimplex(Tuple[SimplexConvertible, Mapping], Protocol):
#   """Protocol class for simplex types with associated data.""" 
#   pass 
PropertySimplex = tuple[SimplexConvertible, Mapping]

@runtime_checkable
class SupportsFaces(Protocol):
  def faces(S: Any, p: int, **kwargs) -> Iterator[Union[SimplexConvertible, PropertySimplex]]:
    raise NotImplementedError 

@runtime_checkable
class Comparable(Protocol):
  """Protocol for annotating comparable types."""
  def __lt__(self, other) -> bool:
    raise NotImplementedError 


@runtime_checkable
class SimplexLike(SimplexConvertible[IT], Comparable, Protocol):
  '''Protocol for _SimplexLike_ types. 

  _SimplexLike_ types are (sized) iterable containers of integer-like types. 
  Consequently, generic methods that rely on enumerating combinations (like faces) or checking 
  length (like dim) work out of the box for the such classes. 
  '''
  def __iter__(self) -> Iterator[IT]: 
    raise NotImplementedError 

@runtime_checkable
class ComplexLike(Collection[SimplexLike], Protocol):
  """Protocol interface for types that represent (abstract) simplicial complexes

  A type is _ComplexLike_ if it implements the Collection[SimplexLike] protocol.
  """
  def __iter__(self) -> Iterator[SimplexLike]: 
    raise NotImplementedError 

@runtime_checkable
class FiltrationLike(SupportsFaces, Protocol):
  """Protocol interface for types that represent _filtered_ simplicial complexes.
  
  A type is _FiltrationLike_ if it implements the Mapping[Any, SimplexLike] protocol. 

  Should support either .faces() -> Union[...] or __iter__() -> (SimplexConvertible, Any)

  Need not 

  """
  def __getitem__(self, k: Any) -> SimplexConvertible:
    pass
  def __iter__(self) -> Iterator[PropertySimplex]:
    pass
  # def index(self, k: Any) -> int:
  #   pass
  def __len__(self) -> int: 
    pass 