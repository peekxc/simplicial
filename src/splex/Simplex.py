from __future__ import annotations
import numpy as np
from numbers import Integral
from dataclasses import dataclass
from sortedcontainers import SortedDict, SortedSet
from .meta import *   

IntType = TypeVar('IntType', bound=Union[int, np.integer, Integral])

@dataclass(frozen=True)
class Simplex(SimplexLike): #  Generic[IntType]
  '''Dataclass for representing a simplex. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 
  
  This class is also SimplexLike.
  
  Magics:
    __hash__  
    __contains__(self, v: int) <=> Returns whether integer 'v' is a vertex in 'self'
  '''
  # __slots__ = 'vertices'
  vertices: tuple[IntType] = cast(tuple([]), tuple[IntType])
  
  def __init__(self, v: SimplexConvertible) -> None:
    t = tuple([int(v)]) if isinstance(v, Number) else tuple(np.unique(np.sort(np.ravel(tuple(v)))))
    object.__setattr__(self, 'vertices', t)
    # assert all([isinstance(v, IntType) for v in self.vertices]), "Simplex must be comprised of integral types."
  
  def __eq__(self, other) -> bool: 
    if len(self) != len(other): return False
    return(all(v == w for (v,w) in zip(iter(self.vertices), iter(other))))
  
  def __len__(self):
    return len(self.vertices)
  
  def __lt__(self, other: Collection[IntType]) -> bool:
    if len(self) >= len(other): 
      return(False)
    else:
      return(all([v in other for v in self.vertices]))
  
  def __le__(self, other: Collection[IntType]) -> bool: 
    if len(self) > len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self < other
  
  def __ge__(self, other: Collection[IntType]) -> bool:
    if len(self) < len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self > other
  
  def __gt__(self, other: Collection[IntType]) -> bool:
    if len(self) <= len(other): 
      return(False)
    else:
      return(all([v in self.vertices for v in other]))
  
  def __contains__(self, __x: IntType) -> bool:
    """ Reports vertex-wise inclusion """
    if not isinstance(__x, Number): 
      return False
    return self.vertices.__contains__(__x)
  
  def __iter__(self) -> Iterable[IntType]:
    return iter(self.vertices)
  
  def __repr__(self):
    return str(self.vertices).replace(',','') if self.dim() == 0 else str(self.vertices).replace(' ','')
  
  def __getitem__(self, index: IntType) -> IntType:
    return self.vertices[index] # auto handles IndexError exception 
  
  def __sub__(self, other) -> Simplex:
    return Simplex(set(self.vertices) - set(Simplex(other).vertices))
  
  def __add__(self, other) -> Simplex:
    return Simplex(set(self.vertices) | set(Simplex(other).vertices))

  def __hash__(self) -> IntType:
    # Because Python has no idea about mutability of an object.
    return hash(self.vertices)

  def faces(self, p: Optional[IntType] = None) -> Iterator[Simplex]:
    dim = len(self.vertices)
    if p is None:
      yield from map(Simplex, chain(*[combinations(self.vertices, d) for d in range(1, dim+1)]))
    else: 
      yield from filter(lambda s: len(s) == p+1, self.faces(None))

  def boundary(self) -> Iterator[Simplex]: 
    if len(self.vertices) == 0: 
      return self.vertices
    yield from map(Simplex, combinations(self.vertices, len(self.vertices)-1))

  def dim(self) -> IntType: 
    return len(self.vertices)-1
    