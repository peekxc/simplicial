## --- GENERICS --- 
import numpy as np 
from numbers import Integral
from .meta import *
# from .complexes import * 
# from .filtrations import * 

def dim(sigma: Union[SimplexConvertible, ComplexLike]) -> int:
  """Returns the dimension of a simplicial object, suitably defined."""
  return sigma.dim() if hasattr(sigma, "dim") else len(sigma) - 1

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
  
def faces(s: Union[SimplexConvertible, ComplexLike], p: int = None) -> Iterator[SimplexConvertible]:
  """
  Returns the faces of a simplicial object, optionally restricted by dimension.

  If _s_ has an existing method _s.faces(p)_, then that method is called with additional keyword args _kwargs_.
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike, then a generator enumerating _p_-combinations of _s_ is created. 
  - if _s_ is ComplexLike, then a generator enumerating _p_-faces of _s_ is created. 
  - if _s_ is FiltrationLike, then a generator enumerating _p_-faces of _s_ in filtration order is created.
  """
  if hasattr(s, "faces"):
    return s.faces(p)
  if isinstance(s, FiltrationLike):
    return(iter(s.values()))
  elif isinstance(s, ComplexLike):
    _ = next(iter(s))
    complex_like = isinstance(_, SimplexConvertible)
    if not complex_like:
      k = len(s)
      if p is None:
        return chain([combinations(s, k-i) for i in reversed(range(1, k))])
      else:
        assert isinstance(p, Integral), f"Invalid type {type(p)}; dimension 'p' must be integral type"
        return (combinations(s, p+1))
    else:
      return iter(s)
  else:
    raise ValueError("Unknown type")