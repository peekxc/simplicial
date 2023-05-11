
import numbers
import numpy as np 

from ..meta import *
from ..combinatorial import * 
from ..generics import *
from ..predicates import *
# from ..Complex import *
from more_itertools import unique_everseen
from collections import Counter

class RankComplex(ComplexLike):
  """Simplicial complex represented via the combinatorial number system.
  
  A rank complex is a simplicial complex that stores simplices as integers (via their ranks) in contiguous memory. The integers 
  are computed by bijecting each p-dimensional simplex to an integer in the range [0, comb(n,p+1))---this process is called _ranking_
  a simplex, and the correspondence between natural numbers and simplices is called the _combinatorial numer system_. 

  Computationally, simplices are stored via ranks as 64-bit unsigned integers in an numpy array, and their vertex representations
  are computed on the fly by inverting the correspondence ('unranking') upon on access. 

  Attributes:
    simplices: structured ndarray of dtype [('rank', uint64), ('dim', uint8)] containing the simplex ranks and dimensions, respectively. 
  """
  def __init__(self, simplices: Iterable[SimplexConvertible] = None) -> None:
    self.s_dtype= np.dtype([('rank', np.uint64), ('dim', np.uint8)])
    if simplices is not None:
      sset = unique_everseen(faces(simplices))
      assert isinstance(simplices, Iterable) and is_repeatable(simplices), "Iterable must be repeatable. A generator is not sufficient!"
      self.simplices = np.unique(np.array([(rank_colex(s), len(s)-1) for s in sset], dtype=self.s_dtype))
    else:
      self.simplices = np.empty(dtype=self.s_dtype, shape=(0,0))

  def __len__(self) -> int: 
    return len(self.simplices)
  
  def __contains__(self, x: SimplexLike) -> bool:
    return rank_colex(x) in self.simplices['rank']
    
  def dim(self) -> int: 
    """The maximal dimension of any simplex in the complex."""
    return np.max(self.simplices['dim'])

  def faces(self, p: int = None) -> Iterable['SimplexLike']:
    """Enumerates the faces of the complex.
    
    Parameters:
      p: optional integer indicating which dimension of faces to enumerate. Default to None (enumerates all faces).
    
    Returns:
      generator which yields on evaluation yields the simplex
    """
    print("WE ARE HERE")
    if p is not None: 
      assert isinstance(p, numbers.Integral)
      p_ranks = self.simplices['rank'][self.simplices['dim'] == p]
      return unrank_combs(p_ranks, k=p+1, order='colex')
    else:
      return unrank_combs(self.simplices['rank'], self.simplices['dim']+1, order='colex')

  def card(self, p: int = None) -> Union[tuple, int]:
    if p is None: 
      return tuple(Counter(self.simplices['dim']).values())
    else: 
      return np.sum(self.simplices['dim'] == p)

  def __iter__(self) -> Iterable[SimplexLike]:
    """Enumerates the faces of the complex."""
    yield from unrank_combs(self.simplices['rank'], self.simplices['dim']+1, order='colex')

  def add(self, simplices: Iterable[SimplexConvertible]): ## TODO: consider array module with numpy array fcasting 
    new_faces = []
    for s in simplices:
      face_ranks = [(rank_colex(f), dim(f)) for f in faces(s)]
      new_faces.extend(face_ranks)
    new_faces = np.array(new_faces, dtype=self.s_dtype)
    self.simplices = np.unique(np.append(self.simplices, new_faces))

  # def cofaces():
  #   pass

  def remove(self, simplices: Iterable[SimplexConvertible]) -> None:
    """Removes simplices from the complex. They must exist.

    If any of the supplied _simplices_ are not in the complex, raise a KeyError.
    """
    faces_to_remove = np.array([(rank_colex(s), dim(s)) for s in simplices], dtype=self.s_dtype)
    in_complex = np.array([s in self.simplices for s in faces_to_remove])
    if any(~in_complex):
      bad = list(simplices)[np.flatnonzero(~in_complex)[0]]
      raise KeyError(f"{bad} not in complex.")
    self.simplices = np.setdiff1d(self.simplices, faces_to_remove)

  def discard(self, simplices: Iterable[SimplexConvertible]) -> None:
    """Removes simplices from the complex, if they exist.
    
    If none of the supplied _simplices_ are in the complex, the simplices are not modified.  
    """
    faces_to_remove = np.array([(rank_colex(s), dim(s)) for s in simplices], dtype=self.s_dtype)
    self.simplices = np.setdiff1d(self.simplices, faces_to_remove)

  def __contains__(self, item: SimplexConvertible) -> bool :
    # s = Simplex(item)
    s = np.array((rank_colex(item),dim(item)), self.s_dtype)
    return self.simplices.__contains__(s)
    # return self.data.__contains__()

  def __len__(self) -> int: 
    return len(self.simplices)
  
  def __repr__(self) -> str:
    if len(self) == 0:
      return "< Empty simplicial complex >"
    return f"{type(self).__name__} with {card(self)} {tuple(range(0,dim(self)+1))}-simplices"

  def __array__(self, dtype=None):
    return self.simplices
  
