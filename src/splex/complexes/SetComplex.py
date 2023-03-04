import numpy as np
from ..meta import * 
from ..Simplex import *
from sortedcontainers import SortedSet 

class SetComplex(ComplexLike):
  """ Abstract Simplicial Complex"""

  def __init__(self, simplices: Iterable[SimplexConvertible] = None):
    """"""
    self.data = SortedSet([], key=lambda s: (len(s), tuple(s), s)) # for now, just use the lex/dim/face order 
    self.n_simplices = tuple()
    self.update(simplices)
  
  ## --- Collection requirements --- 
  def __iter__(self) -> Iterator[Simplex]:
    return iter(self.data)
  
  def __len__(self, p: Optional[int] = None) -> int:
    return len(self.data)

  def __contains__(self, item: Collection[int]):
    return self.data.__contains__(Simplex(item))


  ## --- Generics support --- 
  def dim(self) -> int:
    return len(self.n_simplices) - 1

  def faces(self, p: Optional[int] = None) -> Iterator[Simplex]:
    if p is None:
      yield from iter(self)
    else: 
      assert isinstance(p, Number)
      yield from filter(lambda s: len(s) == p + 1, iter(self))

  def card(self, p: int = None):
    if p is None: 
      return self.n_simplices
    else: 
      assert isinstance(p, int), "Invalid p"
      return 0 if p < 0 or p >= len(self.n_simplices) else self.n_simplices[p]

  def update(self, simplices: Iterable[SimplexLike]):
    for s in simplices:
      self.add(s)

  def add(self, item: Collection[int]):
    # self_set = super(SimplicialComplex, self)
    for face in Simplex(item).faces():
      if not(face in self.data):
        self.data.add(face)
        if len(face) > len(self.n_simplices):
          self.n_simplices = tuple(list(self.n_simplices) + [1])
        else:
          t = self.n_simplices
          self.n_simplices = tuple(t[i]+1 if i == (len(face)-1) else t[i] for i in range(len(t)))
        
  def remove(self, item: Collection[int]):
    self.data.difference_update(set(self.cofaces(item)))
    self._update_shape()

  def discard(self, item: Collection[int]):
    self.data.discard(Simplex(item))
    self._update_shape()
  
  def _update_shape(self) -> None:
    """ Bulk update to shape """
    from collections import Counter
    cc = Counter([len(s)-1 for s in self.data])
    self.shape = tuple(dict(sorted(cc.items())).values())

  def cofaces(self, item: Collection[int]):
    s = Simplex(item)
    yield from filter(lambda t: t >= s, iter(self))