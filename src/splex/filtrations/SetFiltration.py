import numpy as np  
from ..meta import *
from ..Simplex import *
from ..complexes import * 

# Requires: __getitem__, __delitem__, __setitem__ , __iter__, and __len__ a
# Inferred: pop, clear, update, and setdefault
# https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/
class SetFiltration(MutableMapping):
  """Filtered complex of simplices uses _SortedDict_.

  This class represents a filtration of simplices by associating keys of a given index set with _SortedSet_s 
  of _Simplex_ instances. This class also implements the Mapping[Any, SimplexConvertible] 
  Implements: __getitem__, __iter__, __len__, __contains__, keys, items, values, get, __eq__, and __ne__
  """

  @classmethod
  def _key_dim_lex_poset(cls, s: Simplex) -> bool:
    return (len(s), tuple(s), s)

  ## Returns a newly allocated Sorted Set w/ lexicographical poset ordering
  def _sorted_set(self, iterable: Iterable[Collection[Integral]] = None) -> SortedSet:
    key = SetFiltration._key_dim_lex_poset
    return SortedSet(None, key) if iterable is None else SortedSet(iter(map(Simplex, iterable)), key)
  
  def __init__(self, simplices: Union[ComplexLike, Iterable] = None, f: Optional[Callable] = None) -> None:
    """
    Accepts any of the following pairs: 
      (index_iterable, simplices_iterable)
      Iterable[SimplexConvertible], f = None
      Iterable[SimplexConvertible], f = Callable
    """
    self.data = SortedDict()
    self.shape = tuple()
    if isinstance(simplices, ComplexLike):
      if isinstance(f, Callable):
        self += ((f(s), s) for s in simplices)
      elif f is None:
        index_set = np.arange(len(simplices))  
        simplices = sorted(iter(simplices), key=lambda s: (len(s), tuple(s), s)) # dimension, lex, face poset
        self += zip(iter(index_set), simplices)
      else:
        raise ValueError("Invalid input for simplicial complex")
    elif isinstance(simplices, Iterable):
      if isinstance(f, Callable):
        self += ((f(s), s) for s in simplices)
      else:
        self += simplices ## accept pairs, like a normal dict
    elif simplices is None:
      pass
    else: 
      raise ValueError("Invalid input")

  def dim(self) -> int:
    return len(self.shape)-1

  ## delegate new behavior to new methods: __iadd__, __isub__
  def update(self, other: Iterable[Tuple[Any, Collection[Integral]]]):
    for k,v in other:
      self.data.__setitem__(k, self._sorted_set(v))

  def __getitem__(self, key: Any) -> Simplex: 
    return self.data.__getitem__(key)

  def __setitem__(self, k: Any, v: Union[Collection[Integral], SortedSet]):
    self.data.__setitem__(k, self._sorted_set(v))
  
  ## Returns the value of the item with the specified key.
  ## If key doesn't exist, set's F[key] = default and returns default
  def setdefault(self, key, default=None):
    if key in self.data:
      return self[key] # value type 
    else:
      self.__setitem__(key, default)
      return self[key]   # value type   

  def __delitem__(self, k: Any):
    self.data.pop(k)
  
  def __iter__(self) -> Iterator:
    return iter(self.keys())

  def __len__(self) -> int:
    return sum(self.shape)
    #return self.data.__len__()

  # https://peps.python.org/pep-0584/
  def __or__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
    new = self.copy()
    new.update(SortedDict(other))
    return new

  def __ror__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
    new = SortedDict(other)
    new.update(self.data)
    return new

  ## In-place union '|=' operator 
  # TODO: map Collection[Integral] -> SimplexLike? 
  def __ior__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
    self.data.update(other)
    return self
  
  ## In-place append '+=' operator ; true dict union/merge, retaining values
  def __iadd__(self, other: Iterable[Tuple[Any, SimplexLike]]):
    for k,v in other:
      if len(Simplex(v)) >= 1:
        # print(f"key={str(k)}, val={str(v)}")
        s_set = self.setdefault(k, self._sorted_set())
        f = Simplex(v)
        if not(f in s_set):
          s_set.add(f)
          if len(f) > len(self.shape):
            self.shape = tuple(list(tuple(self.shape)) + [1])
          else:
            t = self.shape
            self.shape = tuple(t[i]+1 if i == (len(f)-1) else t[i] for i in range(len(t)))   
    return self

  ## Copy-add '+' operator 
  def __add__(self, other: Iterable[Tuple[int, int]]):
    new = self.copy()
    new += other 
    return new

  ## Simple copy operator 
  def copy(self) -> 'SetFiltration':
    new = SetFiltration()
    from copy import deepcopy
    new.data = deepcopy(self.data)
    new.shape = deepcopy(self.shape)
    return new 

  ## Keys yields the index set. Set expand = True to get linearized order. 
  ## TODO: Make view objects
  def keys(self):
    it_keys = chain()
    for k,v in self.data.items():
      it_keys = chain(it_keys, repeat(k, len(v)))
    return it_keys

  def values(self):
    it_vals = chain()
    for v in self.data.values():
      it_vals = chain(it_vals, iter(v))
    return it_vals

  def items(self):
    it_keys, it_vals = chain(), chain()
    for k,v in self.data.items():
      it_keys = chain(it_keys, repeat(k, len(v)))
      it_vals = chain(it_vals, iter(v))
    return zip(it_keys, it_vals)

  def reindex(self, index_set: Union[Iterable, Callable]) -> None:
    ''' Given a totally ordered key set of the same length of the filtation, or a callable, reindexes the simplices in the filtration '''
    if isinstance(index_set, Iterable):
      assert len(index_set) == len(self), "Index set length not match the number of simplices in the filtration!"
      assert all((i <= j for i,j in pairwise(index_set))), "Index set is not totally ordered!"
      new = SetFiltration(zip(iter(index_set), self.values()))
      self.data = new.data
    elif isinstance(index_set, Callable):
      new = SetFiltration(simplices=self.values(), f=index_set)
      self.data = new.data
    else:
      raise ValueError("invalid index set supplied")

  def faces(self, p: int = None) -> Iterable:
    assert isinstance(p, Integral) or p is None, f"Invalid p:{p} given"
    return self.values() if p is None else filter(lambda s: len(s) == p+1, self.values())

  def __repr__(self) -> str:
    n = len(self.shape)
    return f"{n-1}-d filtered complex with {self.shape}-simplices of dimension {tuple(range(n))}"

  def print(self, **kwargs) -> None:
    import sys
    fv_s, fs_s = [], []
    for k,v in self.items():
      ks = len(str(v))
      fv_s.append(f"{str(k):<{ks}.{ks}}")
      fs_s.append(f"{str(v): <{ks}}")
      assert len(fv_s[-1]) == len(fs_s[-1])
    sym_le, sym_inc = (' ≤ ', ' ⊆ ') if sys.getdefaultencoding()[:3] == 'utf' else (' <= ', ' <= ') 
    print(repr(self), **kwargs)
    print("I: " + sym_le.join(fv_s[:5]) + sym_le + ' ... ' + sym_le + sym_le.join(fv_s[-2:]), **kwargs)
    print("S: " + sym_inc.join(fs_s[:5]) + sym_inc + ' ... ' + sym_inc + sym_inc.join(fs_s[-2:]), **kwargs)

  def __format__(self, format_spec = "default") -> str:
    from io import StringIO
    s = StringIO()
    self.print(file=s)
    res = s.getvalue()
    s.close()
    return res
