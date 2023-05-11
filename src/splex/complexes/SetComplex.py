import numpy as np
from ..meta import * 
from ..Simplex import *
from sortedcontainers import SortedSet # SortedSet is a vaid Sequence! 

class SetComplex(ComplexLike):
  """ Abstract Simplicial Complex"""

  def __init__(self, simplices: Iterable[SimplexConvertible] = None):
    """"""
    self.data = SortedSet([], key=lambda s: (len(s), tuple(s), s)) # for now, just use the lex/dim/face order 
    self.n_simplices = tuple()
    if simplices is not None: 
      self.update(simplices)
  
  ## --- Collection requirements --- 
  def __iter__(self) -> Iterator[Simplex]:
    return iter(self.data)
  
  def __len__(self, p: Optional[int] = None) -> int:
    return len(self.data)

  def __contains__(self, item: Collection[int]):
    return self.data.__contains__(Simplex(item))

  ## --- Sequence requirements --- 
  def __getitem__(self, index: Union[int, slice]):
    return self.data[index]

  # MutableSequence 
  # __getitem__, __setitem__, __delitem__, __len__, insert, append, reverse, extend, pop, remove, and __iadd__

  # MutableSet 
  # __contains__, __iter__, __len__, add, discard, clear, pop, remove, __ior__, __iand__, __ixor__, and __isub__

  ## --- Generics support --- 
  def dim(self) -> int:
    return len(self.n_simplices) - 1

  def faces(self, p: Optional[int] = None) -> Iterator[Simplex]:
    if p is None:
      yield from iter(self)
    else: 
      assert isinstance(p, Number)
      yield from filter(lambda s: len(s) == p + 1, iter(self))

  def card(self, p: int = None) -> tuple:
    if p is None: 
      return tuple(self.n_simplices)
    else: 
      assert isinstance(p, int), "Invalid p"
      return 0 if p < 0 or p >= len(self.n_simplices) else self.n_simplices[p]

  # --- Additional complex support functions ---
  def cofaces(self, item: Collection[int]) -> Iterator[Simplex]:
    s = Simplex(item)
    yield from filter(lambda t: t >= s, iter(self))

  def update(self, simplices: Iterable[SimplexLike]):
    for s in simplices:
      self.add(s)

  def add(self, item: Collection[int]) -> None:
    # self_set = super(SimplicialComplex, self)
    s = Simplex(item)       # cast to Simplex for comparability
    ns = np.zeros(dim(s)+1) # array to update num. simplices
    ns[:len(self.n_simplices)] = self.n_simplices
    for face in faces(s):
      if not(face in self.data):
        self.data.add(face)
        ns[dim(face)] += 1
    self.n_simplices = tuple(ns)
        # if len(face) > len(self.n_simplices):
        #   # self.n_simplices = tuple(list(self.n_simplices) + [1])
        # else:
        #   t = self.n_simplices
          # self.n_simplices = tuple(t[i]+1 if i == (len(face)-1) else t[i] for i in range(len(t)))
        
  def remove(self, item: Collection[int]):
    self.data.difference_update(set(self.cofaces(item)))
    self._update_n_simplices()

  def discard(self, item: Collection[int]):
    self.data.discard(Simplex(item))
    self._update_n_simplices()
  
  def _update_n_simplices(self) -> None:
    """ Bulk update to shape """
    from collections import Counter
    cc = Counter([len(s)-1 for s in self.data])
    self.n_simplices = tuple(dict(sorted(cc.items())).values())