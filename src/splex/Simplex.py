from __future__ import annotations # for mypy to recognize self return types
from numbers import Number, Integral
from typing import *
from .generics import * 

from itertools import * 
from more_itertools import collapse, unique_justseen, seekable, spy
from dataclassy import dataclass
import numpy as np 

@dataclass(frozen=True, slots=True, init=False, repr=False, eq=False)
class SimplexBase: # forget about hashable to make compatible as a data class 
  """Base class for comparable simplex-like classes with integer vertex labels."""
  vertices: Union[tuple[int], Tuple[()]] = ()
  def __init__(self, v: SimplexConvertible):
    object.__setattr__(self, 'vertices', tuple(unique_justseen(sorted(collapse(v)))))
    
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
    """Simplex-wise comparison."""
    if len(self) <= len(other): 
      return(False)
    else:
      return(all([v in self.vertices for v in other]))
  
  def __contains__(self, __x: int) -> bool:
    """Vertex-wise membership test."""
    if not isinstance(__x, Number): 
      return False
    return self.vertices.__contains__(__x)
  
  def __iter__(self) -> Iterator[int]:
    """Vertex-wise iteration."""
    return iter(self.vertices)
  
  def __getitem__(self, index: int) -> int:
    """Vertex-wise indexing."""
    return self.vertices[index] # auto handles IndexError exception 
  
  def __sub__(self, other: SimplexConvertible) -> Simplex:
    """Vertex-wise set difference."""
    return Simplex(set(self.vertices) - set(Simplex(other).vertices))
  
  def __add__(self, other: SimplexConvertible) -> Simplex:
    """Vertex-wise set union."""
    return Simplex(set(self.vertices) | set(Simplex(other).vertices))
  
  def __hash__(self) -> int:
    """ Vertex-wise hashing to support equality tests and hashability """
    return hash(self.vertices)

  def __repr__(self) -> str:
    """ Default str representation prints the vertex labels delimited by commas """
    return str(self.vertices).replace(',','') if self.dim() == 0 else str(self.vertices).replace(' ','')

  def faces(self, p: Optional[int] = None, data: bool = False, **kwargs) -> Iterator[Simplex]: 
    dim: int = len(self.vertices)
    if p is None:
      g = map(Simplex, chain(*[combinations(self.vertices, d) for d in range(1, dim+1)]))
    else: 
      g = map(Simplex, combinations(self.vertices, p+1))
      # g = filter(lambda s: len(s) == p+1, self.faces()) # type: ignore
    return zip_data(g, data)
    # g = g if data == False else handle_data(g, data)
  
  def boundary(self) -> Iterator[Simplex]: 
    if len(self.vertices) == 0: 
      return self.vertices
    yield from map(Simplex, combinations(self.vertices, len(self.vertices)-1))

  def dim(self) -> int: 
    return len(self.vertices)-1

  def __array__(self, dtype = None) -> np.ndarray: 
    """Support native array conversion."""
    dtype = np.uint32 if dtype is None else dtype
    return np.asarray(self.vertices, dtype = dtype)

  def __int__(self) -> int:
    if len(self.vertices) != 1: raise ValueError(f"Invalid conversion of simplex {str(self)} to integer")
    return self.vertices[0]

@dataclass(slots=True, frozen=True, init=False, repr=False, eq=False)
class Simplex(SimplexBase): # , Generic[IT]
  """Simplex dataclass.

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 
  """
  def __init__(self, v: SimplexConvertible):
    # t = tuple(unique_justseen(sorted(collapse(v))))
    super(Simplex, self).__init__(v)
    # object.__setattr__(self, 'vertices', t)

@dataclass(slots=False, frozen=False, init=False, repr=False, eq=False)
class PropertySimplex(SimplexBase):
  """Dataclass for representing a simplex associated with arbitrary properties. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 

  Unlike the _Simplex_ class, this class is neither frozen nor slotted, thus it supports arbitrary field assignments.  
  """
  def __init__(self, v: SimplexConvertible, **kwargs) -> None:
    # super(SimplexBase, self).__init__()
    super(PropertySimplex, self).__init__(v)
    self.__dict__.update(kwargs)
    # object.__setattr__(self, )
  def __setattr__(self, key: str, value: Any) -> None:
    self.__dict__[key] = value



## TODO: Is this entire class not worth it?
## 1. inequality tests become muddled. could inherit all the same behavior but then augment to use value to break ties
## 2. ... but then the value is not a filter value, should be first comparison made 
## 3. boundary and face enumeration become an issue---do they inherit the value? Or are they just simplex's? 
## the former must be done at the filtration class level, whereas the latter can be done simply by downcasts in the process 
## 4. ... the distinction between the typical Simplex is that although a regular simplex in a complex might have faces not taking the same 
## memory as the ones enumerated by a given simplex, we call them equivalent via the hashable equality test. In essence, a Simplex really is a value-type, 
## in the sense that it is an r-type, whereas a Filtered Simplex acts more like an l-value. In the context of C#, (https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), 
## Simplex's are structure types that support value semantics. In contrast, one could have several ValueSimplexes of the same underlying simplex, but different values. 
## Moreover, **two filtrations could have identical ValueSimplexes with different faces/boundaries**
## -----
## Suppose we just inherit all the struct-like behavior of a regular simplex. 
## 1. Equality testing is still vertex-wise. Non-vertex Values are ignored.
## 2. Inequality ordering is unchanged and valid. It is up to the class that uses Value Simplices to ensure they are ordered correctly. 
## 3. boundary and face enumeration would just downcast to simplices / discard values. 
## 4. faces(S, p=1, data=True) would yield something like 
## (o) for s in faces(S, p=1, data=False) => default behavior
## (a) for s,d in faces(S, p=1, data=True) => d is empty dict view {} for Simplex 
## (b) for s,d in faces(S, p=1, data=True) => d is { 'value' : ... } for ValueSimplex 
## (c) for s,d in faces(S, p=1, data=True) => d is dict view for PropertySimplex
## If (b) is changed such that d is a Number type, code would be simpler, but changes the interface. 
## ... https://networkx.org/documentation/stable/developer/nxeps/nxep-0002.html
## S.faces(data=True) should return a FaceDataView such that S.faces(data=True)[s] return the attribute dictionary of s 
## Note: Should use more_itertools Sequence views to support indexing, slicing, and length queries.
## ahh but then, S.faces() should in actuality return a VIEW 
## more_itertools supports constructing SequenceViews which support indexing, slicing, and length queries, though they likely require a Sequence input, 
## which demands __get_item__, which SimplexTree doesn't necessary have. 
## SequenceView's are iterable though, so the contract of faces is still in place. Suggests faces(..., p = Number, ...) could be potentially very multi-pronged:
## - Supports __iter__ + __array__ + __array_interface__ + Sequence + SequenceView + w/ Rank Complex 
## - Supports __iter__ + __array__ + Sequence + SequenceView for SetComplex 
## - Supports __iter__ + __array__ for SimplexTree

@dataclass(slots=True, frozen=True, init=False, repr=False, eq=False)
class ValueSimplex(SimplexBase, Generic[IT]):
  """Dataclass for representing a simplex associated with a single numerical value. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous.

  Unlike the _Simplex_ class, this class is has an additional value slot to change the poset
  """
  value: Number
  def __init__(self, v: SimplexConvertible, value: Number) -> None:
    if not isinstance(value, Number): # todo re-work the order or just consider dtype
      value = np.take(np.squeeze(value),0) if hasattr(value, 'dtype') else value
      value = float(value) if (hasattr(value, '__float__') and not isinstance(value, Number)) else value
      value = int(value) if (hasattr(value, '__int__') and not isinstance(value, Number)) else value
    assert isinstance(value, Number), "Value must be a number"
    t = tuple(unique_justseen(sorted(collapse(v))))
    object.__setattr__(self, 'value', value)
    object.__setattr__(self, 'vertices', t)

  def __repr__(self) -> str:
    idx_str = f"{self.value}" if isinstance(self.value, Integral) else f"{self.value:.2f}"
    return idx_str+":"+str(self.vertices).replace(',','') if self.dim() == 0 else idx_str+":"+str(self.vertices).replace(' ','')
