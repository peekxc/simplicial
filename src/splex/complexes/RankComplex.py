
import numbers
import numpy as np 

from ..meta import *
from ..combinatorial import * 
from ..generics import *
from ..predicates import *

class RankComplex(ComplexLike):
  """Simplicial complex represented via the combinatorial number system.
  
  A rank complex is a simplicial complex that stores simplices as integers (via their ranks) in contiguous memory. The integers 
  are computed by bijecting each p-dimensional simplex to an integer in the range [0, comb(n,p+1))---this process is called _ranking_
  a simplex, and the correspondence between natural numbers and simplices is called the _combinatorial numer system_. 

  Computationally, simplices are stored via ranks as 64-bit unsigned integers in an numpy array, and their vertex representations
  are computed on the fly by inverting the correspondence ('unranking') upon on access. 
  """
  def __init__(self, simplices: Iterable[SimplexConvertible] = None) -> None:
    # simplices = faces(simplices) if isinstance(simplices, ComplexLike) else simplices 
    sset = set()
    for s in simplices: sset |= set(faces(s))
    s_dtype= np.dtype([('rank', np.uint64), ('d', np.uint16)])
    if simplices is not None:
      assert isinstance(simplices, Iterable) and is_repeatable(simplices), "Iterable must be repeatable. A generator is not sufficient!"
      self.simplices = np.unique(np.array([(rank_colex(s), len(s)) for s in sset], dtype=s_dtype))
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


  