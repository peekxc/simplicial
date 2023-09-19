## --- GENERICS --- 
import numpy as np 
from numbers import Integral
from more_itertools import unique_everseen

from .meta import _data_attributes
from .predicates import *

def handle_data(g: Iterable, data: Union[bool, dict, str]) -> Iterable:
  if isinstance(data, bool):
    if data == False: 
      yield from g
    extract_data = lambda e: { attr_name : getattr(e, attr_name) for attr_name in _data_attributes(e) }
    for el in g: 
      yield el, extract_data(el)
    # return zip(g, (extract_data(e) for e in g))
  elif isinstance(data, str):
    for el in g: 
      yield el, getattr(el, data) if hasattr(el, data) else None
  elif isinstance(data, list):
    raise NotImplementedError
  else: 
    raise ValueError(f"Invalid data input of type '{type(data)}'")

def dim(s: Union[SimplexConvertible, ComplexLike], **kwargs) -> int:
  """Returns the dimension of a simplicial object.
  
  If _s_ has an existing method _s.dim(...)_, then that method is called with additional keyword arguments _kwargs_.

  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike with dimension _p_, then _p_ is returned. 
  - if _s_ is ComplexLike, then the largest dimension _p_ of any face in _s_ is returned.
  - if _s_ is none of the above but is Sized, len(_s_) - 1 is returned. 
  """
  if hasattr(s, "dim"):
    return s.dim(**kwargs)
  else:
    if is_complex_like(s):
      return max((dim(s, **kwargs) for s in s))
    else: 
      return len(s) - 1

def boundary(s: Union[SimplexConvertible, ComplexLike], p: int = None, oriented: bool = False, **kwargs) -> Iterable['SimplexConvertible']:
  """
  Returns the boundary of a simplicial object, optionally signed.

  If _s_ has an existing method _s.boundary(p, oriented)_, then that method is called with additional keyword args _kwargs_.

  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike with dimension _p_, then a generator enumerating _(p-1)_-faces of _s_ is created. 
  - if _s_ is ComplexLike, then a sparse boundary matrix whose columns represent boundary chains is returned. 
  - if _s_ is FiltrationLike, then a sparse boundary matrix whose columns represent boundary chains in filtration order is returned.
  - if _s_ is none of the above but is Sized and Iterable, all len(s)-1 combinations are returned of _s_ are returned. 

  TODO: finish this
  """
  if hasattr(s, "boundary"):
    kwargs |= dict(p=p, oriented=oriented)
    return s.boundary(**kwargs)
  return combinations(s, len(s)-1)

def faces(s: Union[SimplexConvertible, ComplexLike], p: int = None, data: bool = False, **kwargs) -> Iterator[Union[SimplexConvertible, PropertySimplexConvertible]]:
  """
  Returns the faces of a simplicial object, optionally restricted by dimension.

  If _s_ has an existing method _s.faces(p)_, then that method is called with additional keyword arguments _kwargs_. 
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike, then a generator enumerating _p_-combinations of _s_ is returned. 
  - if _s_ is ComplexLike, then a generator enumerating _p_-faces of _s_ (in any order) is returned. 
  - if _s_ is FiltrationLike, then a generator enumerating _p_-faces of _s_ in filtration order is returned.
  - if _s_ is none of the above but is Sized and Iterable, all combinations of _s_ of length _p+1_ are chained and returned. 
  """
  kwargs |= dict(p=p, data=data)
  if hasattr(s, "faces"):
    return s.faces(**kwargs)
  elif is_complex_like(s):
    return unique_everseen(chain.from_iterable([faces(f, **kwargs) for f in s])) # handles data implicitly, though faces may not store data
    # if p is None:
    #   g = iter(sset)
    # else: 
    #   g = iter(filter(lambda s: len(s) == p+1, iter(sset)))
  elif is_filtration_like(s):
    if not data:
      return (f for i,f in s)
    else:
      return ((f, dict(index=i)) for i,f in s)
  elif is_simplex_like(s): # is simplex convertible
    k = len(s)
    if p is None:
      g = chain.from_iterable([combinations(s, k-i) for i in reversed(range(0, k))])
    else:
      assert isinstance(p, Integral), f"Invalid type {type(p)}; dimension 'p' must be integral type"
      g = iter(combinations(s, p+1))
    return handle_data(g, data)
  else:
    raise ValueError(f"Unknown type supplied '{type(s)}'")

def card(s: Union[SimplexConvertible, ComplexLike, FiltrationLike], p: int = None, **kwargs):
  """Counts the number of _p_-dimensional simplices of a simplicial object _s_. 
  
  If _s_ has an existing method _s.card(p)_, then that method is called with additional keyword arguments _kwargs_. 

  Otherwise, the behavior of this function depends on the type-class of _s_ and whether _p_ is specified. Namely, 
   - If _s_ is _complex like_, then card(s) returns a tuple containing the number of simplices in _s_ in each dimension, and _card(s, p)_ the number of simplices in _s_ with dimension p.
  """
  if hasattr(s, "card"):
    kwargs |= dict(p=p)
    return s.card(**kwargs)
  else:
    if p is None: 
      from collections import Counter
      cc = Counter([dim(s, **kwargs) for s in faces(s, p, **kwargs)])
      return tuple(cc.values())
    else: 
      assert isinstance(p, int)
      return int(sum([1 for s in faces(s, p, **kwargs) if dim(s, **kwargs) == p]))
    