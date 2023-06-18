import numpy as np
from ..meta import * 
from ..generics import *
from ..Simplex import *
from .Complex_ABCs import Complex 
from sortedcontainers import SortedSet # SortedSet is a vaid Sequence! 

class SetComplex(Complex, ComplexLike):
  """ Abstract Simplicial Complex"""

  def __init__(self, simplices: Iterable[SimplexConvertible] = None):
    """ Set Complex """
    self.data = SortedSet([], key=lambda s: (len(s), tuple(s), s)) # for now, just use the lex/dim/face order 
    self.n_simplices = tuple()
    if simplices is not None: 
      self.update(simplices)
  
  ## --- Collection requirements --- 
  def __iter__(self) -> Iterator[Simplex]:
    """Constructs an iterator of _Simplex_ objects."""
    return iter(self.data)
  
  def __len__(self, p: Optional[int] = None) -> int:
    """Returns the number of (p)-simplices in the complex.
    
    Parameters: 
      p: optional dimension to restrict too. By default, all simplices are counted. 

    Returns: 
      the number of (p)-simplices in the simplex. 
    """
    return len(self.data)

  def __contains__(self, item: Collection[int]):
    """Simplex membership check."""
    return self.data.__contains__(Simplex(item))

  ## --- Sequence requirements ---
  def __getitem__(self, index: Union[int, slice]):
    """Simplex accessor function."""
    return self.data[index]

  # MutableSequence 
  # __getitem__, __setitem__, __delitem__, __len__, insert, append, reverse, extend, pop, remove, and __iadd__

  # MutableSet 
  # __contains__, __iter__, __len__, add, discard, clear, pop, remove, __ior__, __iand__, __ixor__, and __isub__

  ## --- Generics support --- 
  def dim(self) -> int:
    """Returns the maximal dimension of any simplex in the complex."""
    return len(self.n_simplices) - 1

  def faces(self, p: Optional[int] = None, **kwargs) -> Iterator[Simplex]:
    """Enumerates the (p)-faces of the complex."""
    if p is None:
      yield from iter(self)
    else: 
      assert isinstance(p, Number)
      yield from filter(lambda s: len(s) == p + 1, iter(self))

  def card(self, p: int = None) -> tuple:
    """Cardinality of the complex.
    
    If p is supplied, returns the number of p-simplices in the complex. Otherwise, a tuple 
    whose index p represents the number of p-simplices in the complex. 
    """
    if p is None: 
      return self.n_simplices
    else: 
      assert isinstance(p, int), "Invalid p"
      return 0 if p < 0 or p >= len(self.n_simplices) else self.n_simplices[p]

  # --- Additional support functions ---
  def cofaces(self, item: Collection[int]) -> Iterator[Simplex]:
    """Enumerates the cofaces of a give simplex."""
    s = Simplex(item)
    yield from filter(lambda t: t >= s, iter(self))

  def update(self, simplices: Iterable[SimplexConvertible]):
    """Updates the complex by unioning with the given iterable of simplices."""
    for s in simplices:
      self.add(s)

  def add(self, item: SimplexConvertible) -> None:
    """Adds a simplex to the complex.
    
    Note that adding a simplex by definition with add all of its faces to the complex as well.
    """
    s = Simplex(item)                                               # cast to Simplex for comparability
    ns = np.zeros(max(dim(s)+1, dim(self)+1), dtype=np.uint64)      # array to update num. simplices
    ns[:len(self.n_simplices)] = self.n_simplices
    for face in faces(s):
      if face not in self.data:
        self.data.add(face)
        ns[dim(face)] += 1
    self.n_simplices = tuple(ns)
        # if len(face) > len(self.n_simplices):
        #   # self.n_simplices = tuple(list(self.n_simplices) + [1])
        # else:
        #   t = self.n_simplices
          # self.n_simplices = tuple(t[i]+1 if i == (len(face)-1) else t[i] for i in range(len(t)))
        
  def remove(self, item: SimplexConvertible):
    """Removes a simplex from the complex.
    
    Note that removing a simplex by definition with remove all of its cofaces from the complex as well.

    This function raises an exception if the supplied simplex is not found. For non-throwing version, see discard.
    """
    if not self.__contains__(item):
      raise ValueError(f"Simplex {str(Simplex(item))} does not exist in the complex.")
    self.data.difference_update(set(self.cofaces(item)))
    self._update_n_simplices()

  def discard(self, item: SimplexConvertible):
    """Removes a simplex from the complex.
    
    Note that removing a simplex by definition with remove all of its cofaces from the complex as well.
    """
    self.data.difference_update(set(self.cofaces(item)))
    self._update_n_simplices()
  
  def _update_n_simplices(self) -> None:
    """ Bulk update to shape """
    from collections import Counter
    cc = Counter([len(s)-1 for s in self.data])
    self.n_simplices = tuple(dict(sorted(cc.items())).values())

  def __repr__(self):
    if len(self) == 0:
      return "<  Empty set complex >"
    return f"Set Complex with {card(self)} {tuple(range(0,dim(self)+1))}-simplices"