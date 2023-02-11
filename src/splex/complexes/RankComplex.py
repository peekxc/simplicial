
import numbers
import numpy as np 

from ..meta import *
from ..combinatorial import * 

class RankComplex(ComplexLike):
  """Simplicial complex represented via the combinatorial number system.
  
  """
  def __init__(self, simplices: Iterable[SimplexConvertible] = None) -> None:
    simplices = list(simplices.faces()) if isinstance(simplices, ComplexLike) else simplices 
    s_dtype= np.dtype([('rank', np.uint64), ('d', np.uint16)])
    if simplices is not None:
      assert isinstance(simplices, Iterable) and not(iter(simplices) is simplices), "Iterable must be repeatable. A generator is not sufficient!"
      self.simplices = np.unique(np.array([(rank_colex(s), len(s)) for s in simplices], dtype=s_dtype))
    else:
      self.simplices = np.empty(dtype=s_dtype)

  def __len__(self) -> int: 
    return len(self.simplices)
  
  def __contains__(self, x: SimplexLike) -> bool:
    return rank_colex(x) in self.simplices['rank']
    
  def dim(self) -> int: 
    return max(self.simplices['d'])-1

  def faces(self, p: int = None) -> Iterable['SimplexLike']:
    if p is not None: 
      assert isinstance(p, numbers.Integral)
      yield from unrank_combs(self.simplices['rank'][self.simplices['d'] == (p+1)], k=p+1)
    else:
      yield from unrank_combs(self.simplices['rank'], self.simplices['d'])

  def __iter__(self) -> Iterable[SimplexLike]:
    yield from unrank_combs(self.simplices['rank'], self.simplices['d'])


  