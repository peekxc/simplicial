from __future__ import annotations # for mypy to recognize self return types
from numbers import Number, Integral
from dataclasses import dataclass
from more_itertools import collapse, unique_justseen
from .meta import *   

class SimplexBase(Hashable):
  vertices: Union[tuple[int], Tuple[()]] = ()

  def __eq__(self, other: object) -> bool: 
    if not isinstance(other, SimplexConvertible):
      return False
    if len(self) != len(other): return False
    return(all(v == w for (v, w) in zip(iter(self.vertices), iter(other))))
  
  def __len__(self) -> int:
    return len(self.vertices)
  
  def __lt__(self, other: SimplexConvertible[IT]) -> bool:
    if len(self) >= len(other): 
      return(False)
    else:
      return(all([v in other for v in self.vertices]))
  
  def __le__(self, other: Collection[IT]) -> bool: 
    if len(self) > len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self < other
  
  def __ge__(self, other: Collection[IT]) -> bool:
    if len(self) < len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self > other
  
  def __gt__(self, other: Collection[IT]) -> bool:
    if len(self) <= len(other): 
      return(False)
    else:
      return(all([v in self.vertices for v in other]))
  
  def __contains__(self, __x: int) -> bool:
    """ Reports vertex-wise inclusion """
    if not isinstance(__x, Number): 
      return False
    return self.vertices.__contains__(__x)
  
  def __iter__(self) -> Iterator[int]:
    return iter(self.vertices)
  
  def __repr__(self) -> str:
    return str(self.vertices).replace(',','') if self.dim() == 0 else str(self.vertices).replace(' ','')
  
  def __getitem__(self, index: int) -> int:
    return self.vertices[index] # auto handles IndexError exception 
  
  def __sub__(self, other: SimplexConvertible) -> Simplex:
    return Simplex(set(self.vertices) - set(Simplex(other).vertices))
  
  def __add__(self, other: SimplexConvertible) -> Simplex:
    return Simplex(set(self.vertices) | set(Simplex(other).vertices))

  def __hash__(self) -> int:
    # Because Python has no idea about mutability of an object.
    return hash(self.vertices)

  def faces(self, p: Optional[int] = None) -> Iterator[Simplex]:
    dim: int = len(self.vertices)
    if p is None:
      yield from map(Simplex, chain(*[combinations(self.vertices, d) for d in range(1, dim+1)]))
    else: 
      yield from filter(lambda s: len(s) == p+1, self.faces()) # type: ignore

  def boundary(self) -> Iterator[Simplex]: 
    if len(self.vertices) == 0: 
      return self.vertices
    yield from map(Simplex, combinations(self.vertices, len(self.vertices)-1))

  def dim(self) -> int: 
    return len(self.vertices)-1
    

@dataclass(frozen=True, slots=True, init=False, repr=False, eq=False)
class Simplex(SimplexBase, Generic[IT]):
  '''Dataclass for representing a simplex. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 
  '''
  def __init__(self, v: SimplexConvertible) -> None:
    t = tuple(unique_justseen(sorted(collapse(v))))
    object.__setattr__(self, 'vertices', t)

@dataclass(frozen=True, slots=True, init=False, repr=False, eq=False)
class ValueSimplex(SimplexBase, Generic[IT]):
  '''Dataclass for representing a simplex associated with a value. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 
  '''
  value: Number
  def __init__(self, v: SimplexConvertible, value: Number) -> None:
    t = tuple(unique_justseen(sorted(collapse(v))))
    object.__setattr__(self, 'value', value)
    object.__setattr__(self, 'vertices', t)

  def __repr__(self) -> str:
    idx_str = f"{self.value}" if isinstance(self.value, Integral) else f"{self.value:.2f}"
    return idx_str+":"+str(self.vertices).replace(',','') if self.dim() == 0 else idx_str+":"+str(self.vertices).replace(' ','')
  

@dataclass(frozen=False, slots=False, init=False, repr=False, eq=False)
class PropertySimplex(SimplexBase):
  def __init__(self, v: SimplexConvertible) -> None:
    super(SimplexBase, self).__init__()
    t = tuple(unique_justseen(sorted(collapse(v))))
    object.__setattr__(self, 'vertices', t)