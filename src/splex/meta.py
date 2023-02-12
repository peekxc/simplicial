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

# Based on https://www.timekl.com/blog/2014/12/14/learning-swift-convertibles/
@runtime_checkable
class SimplexConvertible(Collection[Integral], Hashable, Protocol):
  """Protocol class for simplex-convertible types. 
  
  Any hashable collection is convertible to a Simplex type. The minimal overloads include: 
    __contains__ 
    __iter__
    __len__
    __hash__ 
  """
  pass


@runtime_checkable
class Comparable(Protocol):
  """Protocol for annotating comparable types."""
  @abstractmethod
  def __lt__(self, other) -> bool:
      pass 

@runtime_checkable
class SetLike(Comparable, Container, Protocol):
  """Protocol for annotating set-like types."""
  pass

@runtime_checkable
class SimplexLike(SimplexConvertible, SetLike, Protocol):
  '''Protocol for _SimplexLike_ types. 

  _SimplexLike_ types are (sized) iterable containers of SimplexConvertible types. 
  Consequently, generic methods that rely on enumerating combinations (like faces) or checking 
  length (like dim) work out of the box for the such classes. 
  '''
  ...


@runtime_checkable
class ComplexLike(Collection[SimplexLike], Protocol):
  """Protocol interface for types that represent (abstract) simplicial complexes

  A type is _ComplexLike_ if it implements the Collection[SimplexLike] protocol.
  """
  def __iter__(self) -> Iterator[SimplexLike]: 
    raise NotImplementedError 

@runtime_checkable
class FiltrationLike(Protocol):
  """Protocol interface for types that represent (abstract) simplicial complexes 
  
  A type is _FiltrationLike_ if it implements the Mapping[Any, SimplexLike] protocol. 
  """
  def keys(self) -> Iterable[Any]:
    pass
  def values(self) -> Iterable[SimplexLike]:
    raise NotImplementedError
  def __getitem__(self, k: Any) -> SimplexLike:
    pass
  def __iter__(self) -> Iterator[Any]:
    pass
  def __len__(self) -> int: 
    pass 