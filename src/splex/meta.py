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
# FT = TypeVar('FT', float, np.floating, Number, covariant=True)

def _data_attributes(s: Any) -> list: 
  slots = list(chain.from_iterable(getattr(cls, '__slots__', []) for cls in type(s).__mro__))
  attributes = [attr for attr in filter(lambda a: a[0] != "_", dir(s)) if not isinstance(getattr(s, attr), Callable)]
  attributes = set(slots) | set(attributes)
  return list(sorted(attributes))

# Based on https://www.timekl.com/blog/2014/12/14/learning-swift-convertibles/
@runtime_checkable
class SimplexConvertible(Collection, Protocol[IT]):
  """Protocol class for simplex-convertible types. 
  
  Any collection of integer-like values is convertible to a Simplex type.
  """
  pass

PropertySimplexConvertible = tuple[SimplexConvertible, Mapping]


@runtime_checkable
class SupportsFaces(Protocol):
  def faces(S: Any, p: int, **kwargs) -> Iterator[Union[SimplexConvertible, PropertySimplexConvertible]]:
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

  A type is _ComplexLike_ if it implements the Collection[SimplexLike] protocol. (contains, iter, len)
  """
  def __iter__(self) -> Iterator[SimplexLike]: 
    raise NotImplementedError 

## Python typing is just not strong enough to use isinstance with @runtime_checkable.
## Need to be able to peek at an iterable and see something about it. 
# def is_simplex_like() -> bool:



# def is_complex_like(S: ComplexLike) -> bool:
#   if not isinstance(S, ComplexLike): return False # checks __iter__
#   from more_itertools import spy
#   spy()



@runtime_checkable
class FiltrationLike(SupportsFaces, Collection, Protocol):
  """Protocol interface for types that represent _filtered_ simplicial complexes.
  
  A type is _FiltrationLike_ if it implements Sequence protocol. 

  Should support either .faces() -> Union[...] or __iter__() -> (SimplexConvertible, Any)

  """
  ## --- Collection requirements ---
  def __len__(self) -> int: 
    raise NotImplementedError  
  def __iter__(self) -> Iterator[tuple]:
    raise NotImplementedError 
  def __contains__(self, item):
    raise NotImplementedError 

  ## --- Sequence requirements --- 
  def __getitem__(self, index) -> tuple:
    raise NotImplementedError

  # --- Set requirements --- 

  # --- Mutable Set --- 

  ## --- Sequence mixins --- 
  # def index(self, k: Any) -> int:
  #   raise NotImplementedError 
  # def __reversed__(self): -> Iterator[PropertySimplex]:
  #   pass

