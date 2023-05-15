
import numbers
import numpy as np 

from ..meta import *
from ..combinatorial import * 
from ..generics import *
from ..predicates import *
from ..Simplex import *
# from ..Complex import *
from more_itertools import unique_everseen
from collections import Counter
from .Complex_ABCs import Complex

class RankComplex(Complex, Sequence, ComplexLike):
  """Simplicial complex represented via the combinatorial number system.
  
  A rank complex is a simplicial complex that stores simplices as integers (via their ranks) in contiguous memory. The integers 
  are computed by bijecting each p-dimensional simplex to an integer in the range [0, comb(n,p+1))---this process is called _ranking_
  a simplex, and the correspondence between natural numbers and simplices is called the _combinatorial numer system_. 

  Computationally, simplices are stored via ranks as 64-bit unsigned integers in an numpy array, and their vertex representations
  are computed on the fly by inverting the correspondence ('unranking') upon on access. 

  Attributes:
    simplices: structured ndarray of dtype [('rank', uint64), ('dim', uint8)] containing the simplex ranks and dimensions, respectively. 
  """
  
  @staticmethod 
  def _str_rank(item: SimplexConvertible) -> tuple:
    return rank_colex(item), dim(item)

  def __init__(self, simplices: Iterable[SimplexConvertible] = None) -> None:
    """"""
    # simplices = faces(simplices) if isinstance(simplices, ComplexLike) else simplices 
    sset = unique_everseen(faces(simplices))
    self.s_dtype = np.dtype([('rank', np.uint64), ('dim', np.uint16)])
    if simplices is not None:
      sset = unique_everseen(faces(simplices))
      assert isinstance(simplices, Iterable) and is_repeatable(simplices), "Iterable must be repeatable. A generator is not sufficient!"
      self.simplices = np.unique(np.array([RankComplex._str_rank(s) for s in sset], dtype=self.s_dtype))
    else:
      self.simplices = np.empty(dtype=self.s_dtype, shape=(0,0))

  def __len__(self) -> int: 
    return len(self.simplices)
  
  def __contains__(self, x: SimplexConvertible) -> bool:
    return rank_colex(x) in self.simplices['rank']
    
  def dim(self) -> int: 
    """The maximal dimension of any simplex in the complex."""
    return np.max(self.simplices['dim'])

  def faces(self, p: int = None, **kwargs) -> Iterable['SimplexLike']:
    """Enumerates the faces of the complex.
    
    Parameters:
      p: optional integer indicating which dimension of faces to enumerate. Default to None (enumerates all faces).
    
    Returns:
      generator which yields on evaluation yields the simplex
    """
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

  def __getitem__(self, index: Union[int, slice]) -> Union[SimplexConvertible, Iterable]:
    """Retrieves a simplex at some index position. 
    
    Note this constructs the simplex on demand from its rank information. 
    """
    if isinstance(index, Integral):
      s = unrank_colex(self.simplices['rank'][index], self.simplices['dim'][index]+1)
      return Simplex(s)
    elif isinstance(index, slice):
      return map(Simplex, unrank_combs(self.simplices['rank'][index], self.simplices['dim'][index]+1, order='colex'))
    else:
      raise ValueError(f"Invalid index type '{type(index)}' given.")

  def add(self, item: SimplexConvertible) -> None: ## TODO: consider array module with numpy array fcasting 
    """Adds a simplex and its faces to the complex, if they do not already exist.
    
    If _item_ is already in the complex, the underlying complex is not modified. 
    """
    if item not in self:
      face_ranks = np.array([RankComplex._str_rank(f) for f in faces(item)], dtype=self.s_dtype)
      self.simplices = np.unique(np.append(self.simplices, face_ranks))
    # new_faces = []
    # for s in simplices:
    #   face_ranks = [RankComplex._str_rank(f) for f in faces(s)]
    #   new_faces.extend(face_ranks)
    # new_faces = np.array(new_faces, dtype=self.s_dtype)
    # self.simplices = np.unique(np.append(self.simplices, new_faces))

  def cofaces(self, item: SimplexConvertible):
    s = Simplex(item)
    yield from filter(lambda t: Simplex(t) >= s, iter(self))

  ## TODO: need to add cofaces to enable remove 
  ## TODO: distinguish simplex convertible from Iterable of simplices--need to revisit the predicates
  def remove(self, item: SimplexConvertible) -> None:
    """Removes simplices from the complex. They must exist.

    If any of the supplied _simplices_ are not in the complex, raise a KeyError.
    """
    s_item = np.array([RankComplex._str_rank(item)], dtype=self.s_dtype)
    if s_item not in self.simplices:
      raise KeyError(f"{str(item)} not in complex.")
    s_cofaces = np.array([RankComplex._str_rank(item) for f in self.cofaces(item)], dtype=self.s_dtype)
    self.simplices = np.setdiff1d(self.simplices, s_cofaces)
    # faces_to_remove = np.array([(rank_colex(s), dim(s)) for s in simplices], dtype=self.s_dtype)
    # in_complex = np.array([s in self.simplices for s in faces_to_remove])
    # if any(~in_complex):
    #   bad = list(simplices)[np.flatnonzero(~in_complex)[0]]
    #   raise KeyError(f"{bad} not in complex.")
    # self.simplices = np.setdiff1d(self.simplices, faces_to_remove)

  def discard(self, item: SimplexConvertible) -> None:
    """Removes simplices from the complex, if they exist.
    
    If none of the supplied _simplices_ are in the complex, the simplices are not modified.  
    """
    s_cofaces = np.array([RankComplex._str_rank(f) for f in self.cofaces(item)], dtype=self.s_dtype)
    if len(s_cofaces) > 0:
      self.simplices = np.setdiff1d(self.simplices, s_cofaces)

  def __contains__(self, item: SimplexConvertible) -> bool:
    # s = Simplex(item)
    s = np.array([RankComplex._str_rank(item)], self.s_dtype)
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
  
