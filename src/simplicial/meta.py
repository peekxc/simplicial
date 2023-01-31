from __future__ import annotations
from abc import abstractmethod
from typing import *
from itertools import *
from functools import total_ordering
from numbers import Number
from numpy.typing import ArrayLike
from collections.abc import Set, Hashable

@runtime_checkable
class Comparable(Protocol):
  """Protocol for annotating comparable types."""
  @abstractmethod
  def __lt__(self, other) -> bool:
      pass

@runtime_checkable
class SetLike(Comparable, Protocol):
  """Protocol for annotating set-like types."""
  @abstractmethod
  def __contains__(self, item: Any) -> bool: pass
  
  @abstractmethod
  def __iter__(self) -> Iterator[Any]: pass
  
  @abstractmethod
  def __len__(self) -> int: pass
    
@runtime_checkable
class Sequence(Collection, Sized, Protocol):
  def __getitem__(self, index): raise NotImplementedError

@runtime_checkable
class MutableSequence(Sequence, Protocol):
  def __delitem__(self, index): raise NotImplementedError
  def __setitem__(self, key, newvalue): raise NotImplementedError


## --- Protocol classes --- 
@runtime_checkable
class SimplexLike(SetLike, Hashable, Protocol):
  ''' 
  An object is SimplexLike if it is Immutable, Hashable, and SetLike

  By definition, this implies a simplex is sized, iterable, and acts as a container (supports vertex __contains__ queries)

  Protocols: SetLike[Container, Comparable], Hashable, Immutable
  Abstract Methods: __hash__, __contains__, __len__, __iter__, __setitem__
  '''
  # def __setitem__(self, *args) -> None:
  #   raise TypeError("'simplex' object does not support item assignment")

@runtime_checkable
class ComplexLike(Collection['SimplexLike'], Protocol):
  ''' 
  An object is ComplexLike if it is a iterable collection of SimplexLike objects and it has dim() and faces() methods.
  
  Protocols: Collection[Sized, Iterable, Container]
  Methods: __contains__, __iter__, __len__
  '''
  def __iter__(self) -> Iterable['SimplexLike']: 
    raise NotImplementedError 
  def __next__(self) -> SimplexLike:
    raise NotImplementedError
  def dim(self) -> int: 
    raise NotImplementedError
  def faces(self, p: int) -> Iterable['SimplexLike']:
    raise NotImplementedError

@runtime_checkable
class FiltrationLike(ComplexLike, Sequence['SimplexLike'], Protocol):
  """ An object is FiltrationLike if it is ComplexLike and is a Sequence of SimplexLike objects. """
  def __reversed__(self) -> Iterable['SimplexLike']:
    raise NotImplementedError
  def index(self, other: SimplexLike) -> int:
    raise NotImplementedError