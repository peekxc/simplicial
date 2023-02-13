import numpy as np
from ..meta import * 
from ..Simplex import *
from sortedcontainers import SortedSet 

## TODO: implement a simplex |-> attribute system like networkx graphs
class SetComplex(ComplexLike):
  """ Abstract Simplicial Complex"""

  def __init__(self, simplices: Iterable[SimplexConvertible] = None):
    """"""
    self.data = SortedSet([], key=lambda s: (len(s), tuple(s), s)) # for now, just use the lex/dim/face order 
    self.shape = tuple()
    self.update(simplices)
  
  def __len__(self, p: Optional[int] = None) -> int:
    return len(self.data)

  def __contains__(self, item: Collection[int]):
    return self.data.__contains__(Simplex(item))

  def __iter__(self) -> Iterator:
    return iter(self.data)
  
  def dim(self) -> int:
    return len(self.shape) - 1

  def faces(self, p: Optional[int] = None) -> Iterable['Simplex']:
    if p is None:
      yield from iter(self)
    else: 
      assert isinstance(p, Number)
      yield from filter(lambda s: len(s) == p + 1, iter(self))

  def card(self, p: int = None):
    if p is None: 
      return self.shape
    else: 
      assert isinstance(p, int), "Invalid p"
      return 0 if p < 0 or p >= len(self.shape) else self.shape[p]

  def update(self, simplices: Iterable[SimplexLike]):
    for s in simplices:
      self.add(s)

  def add(self, item: Collection[int]):
    # self_set = super(SimplicialComplex, self)
    for face in Simplex(item).faces():
      if not(face in self.data):
        self.data.add(face)
        if len(face) > len(self.shape):
          self.shape = tuple(list(self.shape) + [1])
        else:
          t = self.shape
          self.shape = tuple(t[i]+1 if i == (len(face)-1) else t[i] for i in range(len(t)))
        
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

  def __repr__(self) -> str:
    if self.data.__len__() <= 15:
      return repr(self.data)
    else:
      from collections import Counter
      cc = Counter([s.dim() for s in iter(self)])
      cc = dict(sorted(cc.items()))
      return f"{max(cc)}-d complex with {tuple(cc.values())}-simplices of dimension {tuple(cc.keys())}"

  def __format__(self, format_spec = "default") -> str:
    from io import StringIO
    s = StringIO()
    self.print(file=s)
    res = s.getvalue()
    s.close()
    return res

  def print(self, **kwargs) -> None:
    ST = np.zeros(shape=(self.__len__(), self.dim()+1), dtype='<U15')
    ST.fill(' ')
    for i,s in enumerate(self):
      ST[i,:len(s)] = str(s)[1:-1].split(',')
    SC = np.apply_along_axis(lambda x: ' '.join(x), axis=0, arr=ST)
    for i, s in enumerate(SC): 
      ending = '\n' if i != (len(SC)-1) else ''
      print(s, sep='', end=ending, **kwargs)

# Pythonic version: https://grantjenks.com/docs/sortedcontainers/#features

# The OrderedDict was designed to be good at reordering operations. Space efficiency, iteration speed, and the performance of update operations were secondary.
# A mapping object maps hashable values to arbitrary objects
# https://stackoverflow.com/questions/798442/what-is-the-correct-or-best-way-to-subclass-the-python-set-class-adding-a-new