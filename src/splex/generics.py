## --- GENERICS --- 
import numpy as np 
from numbers import Integral
from more_itertools import unique_everseen
from .meta import *
# from .complexes import * 
# from .filtrations import * 



def dim(sigma: Union[SimplexConvertible, ComplexLike], **kwargs) -> int:
  """Returns the dimension of a simplicial object, suitably defined."""
  if hasattr(sigma, "dim"):
    return sigma.dim(**kwargs)
  else:
    complex_like = isinstance(next(iter(sigma)), SimplexConvertible) # first element is simplexconvertible -> complexLike
    if complex_like:
      return max((dim(s, **kwargs) for s in sigma))
    else: 
      return len(sigma) - 1

def boundary(s: Union[SimplexConvertible, ComplexLike], p: int = None, oriented: bool = False, **kwargs) -> Iterable['SimplexConvertible']:
  """
  Returns the boundary of a simplicial object, optionally signed.

  If _s_ has an existing method _s.boundary(p, oriented)_, then that method is called with additional keyword args _kwargs_.
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike with dimension _p_, then a generator enumerating _(p-1)_-faces of _s_ is created. 
  - if _s_ is ComplexLike, then a sparse boundary matrix whose columns represent boundary chains is returned. 
  - if _s_ is FiltrationLike, then a sparse boundary matrix whose columns represent boundary chains in filtration order is returned.

  """
  if hasattr(s, "boundary"):
    return s.boundary(**kwargs)
  return combinations(s, len(s)-1)


def faces(s: Union[SimplexConvertible, ComplexLike], p: int = None, **kwargs) -> Iterator[Union[SimplexConvertible, PropertySimplexConvertible]]:
  """
  Returns the faces of a simplicial object, optionally restricted by dimension.

  If _s_ has an existing method _s.faces(p)_, then that method is called with additional keyword args _kwargs_.
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike, then a generator enumerating _p_-combinations of _s_ is created. 
  - if _s_ is ComplexLike, then a generator enumerating _p_-faces of _s_ is created. 
  - if _s_ is FiltrationLike, then a generator enumerating _p_-faces of _s_ in filtration order is created.
  """
  if hasattr(s, "faces"):
    return s.faces(p, **kwargs)
  if isinstance(s, FiltrationLike):
    return(iter(s.values()))
  elif isinstance(s, ComplexLike):
    complex_like = isinstance(next(iter(s)), SimplexConvertible) # first element is simplexconvertible -> complexLike
    if complex_like:
      sset = unique_everseen(chain.from_iterable([faces(f, **kwargs) for f in s]))
      if p is None:
        return iter(sset)
      else: 
        return iter(filter(lambda s: len(s) == p+1, iter(sset)))
    else: # is simplex convertible
      k = len(s)
      if p is None:
        return chain.from_iterable([combinations(s, k-i) for i in reversed(range(0, k))])
      else:
        assert isinstance(p, Integral), f"Invalid type {type(p)}; dimension 'p' must be integral type"
        return iter(combinations(s, p+1))
  else:
    raise ValueError("Unknown type")

def card(s: Union[SimplexConvertible, ComplexLike, FiltrationLike], p: int = None, **kwargs):
  if hasattr(s, "card"):
    return s.card(p)
  else:
    if p is None: 
      from collections import Counter
      cc = Counter([dim(s, **kwargs) for s in faces(s, p, **kwargs)])
      return tuple(cc.values())
    else: 
      assert isinstance(p, int)
      return int(sum([1 for s in faces(s, p, **kwargs) if dim(s, **kwargs) == p]))