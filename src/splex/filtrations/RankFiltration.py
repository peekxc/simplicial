
import numbers
import numpy as np 

from ..meta import *
from combin import *

class RankFiltration(FiltrationLike):
  def __init__(self, simplices: Union[ComplexLike, Iterable], f: Callable = None):
    # simplices = list(simplices.faces()) if isinstance(simplices, ComplexLike) else simplices 
    # assert isinstance(simplices, Iterable) and not(iter(simplices) is simplices), "Iterable must be repeatable. A generator is not sufficient!"
    if f is not None:
      s_dtype= np.dtype([('rank', np.uint64), ('d', np.uint16), ('f', np.float64)])
      self.simplices = np.array([(rank_colex(s), len(s), f(s)) for s in simplices], dtype=s_dtype)
    else: 
      s_dtype= np.dtype([('rank', np.uint64), ('d', np.uint16), ('f', np.uint32)])
      self.simplices = np.array([(rank_colex(s), len(s), i) for i, s in enumerate(simplices)], dtype=s_dtype)
  
  def reindex(self, f: Callable['SimplexLike', Any]) -> None:
    # self.w = np.array([f(s) for s in iter(self)])
    ind = np.argsort(self.w, order=('f', 'd', 'r'))
    self.simplices = self.simplices[ind]

#   ## Mapping interface
#   __iter__ = lambda self: iter(self.simplices['f'])
#   def __getitem__(self, k) -> SimplexLike: 
#     i = np.searchsorted(self.simplices['f'])
#     r,d,f = self.simplices[i][:2]
#     return unrank_colex(r, d)
  
#   ## Mapping mixins
#   keys = lambda self: iter(self.simplices['f'])
#   values = lambda self: self.faces()
#   items = lambda self: zip(self.keys(), self.values())
#   __eq__ = lambda self, other: all(self.simplices == other.simplices) if len(self.simplices) == len(other.simplices) else False
#   __ne__ = lambda self, other: any(self.simplices != other.simplices) if len(self.simplices) == len(other.simplices) else False


  ## MutableMapping Interface 
  # __setitem__, __delitem__, pop, popitem, clear, update, setdefault

# class MutableCombinatorialFiltration(CombinatorialComplex, Mapping):

    #   self.simplices = simplices
    #   self.indices = range(len(simplices)) if I is None else I
    #   assert all([isinstance(s, SimplexLike) for s in simplices]), "Must all be simplex-like"
    #   if I is not None: assert len(simplices) == len(I)
    #   self.simplices = [Simplex(s) for s in simplices]
    #   self.index_set = np.arange(0, len(simplices)) if I is None else np.asarray(I)
    #   self.dtype = [('s', Simplex), ('index', I.dtype)]
    # self.data = SortedDict()
    # self.shape = tuple()
    # if isinstance(iterable, SimplicialComplex):
    #   if isinstance(f, Callable):
    #     self += ((f(s), s) for s in iterable)
    #   elif f is None:
    #     index_set = np.arange(len(iterable))  
    #     iterable = sorted(iter(iterable), key=lambda s: (len(s), tuple(s), s)) # dimension, lex, face poset
    #     self += zip(iter(index_set), iterable)
    #   else:
    #     raise ValueError("Invalid input for simplicial complex")
    # elif isinstance(iterable, Iterable):
    #   self += iterable ## accept pairs, like a normal dict
    # elif iterable is None:
    #   pass
    # else: 
    #   raise ValueError("Invalid input")

  # ## delegate new behavior to new methods: __iadd__, __isub__
  # def update(self, other: Iterable[Tuple[Any, Collection[Integral]]]):
  #   for k,v in other:
  #     self.data.__setitem__(k, self._sorted_set(v))

  # def __getitem__(self, key: Any) -> Simplex: 
  #   return self.data.__getitem__(key)

  # def __setitem__(self, k: Any, v: Union[Collection[Integral], SortedSet]):
  #   self.data.__setitem__(k, self._sorted_set(v))
  
  # ## Returns the value of the item with the specified key.
  # ## If key doesn't exist, set's F[key] = default and returns default
  # def setdefault(self, key, default=None):
  #   if key in self.data:
  #     return self[key] # value type 
  #   else:
  #     self.__setitem__(key, default)
  #     return self[key]   # value type   

  # def __delitem__(self, k: Any):
  #   self.data.__del__(k)
  
  # def __iter__(self) -> Iterator:
  #   return iter(self.keys())

  # def __len__(self) -> int:
  #   return sum(self.shape)
  #   #return self.data.__len__()

  # # https://peps.python.org/pep-0584/
  # def __or__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
  #   new = self.copy()
  #   new.update(SortedDict(other))
  #   return new

  # def __ror__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
  #   new = SortedDict(other)
  #   new.update(self.data)
  #   return new

  # ## In-place union '|=' operator 
  # # TODO: map Collection[Integral] -> SimplexLike? 
  # def __ior__(self, other: Union[Iterable[Tuple[int, int]], Mapping]):
  #   self.data.update(other)
  #   return self
  
  # ## In-place append '+=' operator ; true dict union/merge, retaining values
  # def __iadd__(self, other: Iterable[Tuple[int, int]]):
  #   for k,v in other:
  #     if len(Simplex(v)) >= 1:
  #       # print(f"key={str(k)}, val={str(v)}")
  #       s_set = self.setdefault(k, self._sorted_set())
  #       f = Simplex(v)
  #       if not(f in s_set):
  #         s_set.add(f)
  #         if len(f) > len(self.shape):
  #           self.shape = tuple(list(tuple(self.shape)) + [1])
  #         else:
  #           t = self.shape
  #           self.shape = tuple(t[i]+1 if i == (len(f)-1) else t[i] for i in range(len(t)))   
  #   return self

  # ## Copy-add '+' operator 
  # def __add__(self, other: Iterable[Tuple[int, int]]):
  #   new = self.copy()
  #   new += other 
  #   return new

  # ## Simple copy operator 
  # def copy(self) -> 'MutableFiltration':
  #   new = MutableFiltration()
  #   new.data = self.data.copy()
  #   new.shape = self.shape.copy()
  #   return new 

  # ## Keys yields the index set. Set expand = True to get linearized order. 
  # ## TODO: Make view objects
  # def keys(self):
  #   it_keys = chain()
  #   for k,v in self.data.items():
  #     it_keys = chain(it_keys, repeat(k, len(v)))
  #   return it_keys

  # def values(self):
  #   it_vals = chain()
  #   for v in self.data.values():
  #     it_vals = chain(it_vals, iter(v))
  #   return it_vals

  # def items(self):
  #   it_keys, it_vals = chain(), chain()
  #   for k,v in self.data.items():
  #     it_keys = chain(it_keys, repeat(k, len(v)))
  #     it_vals = chain(it_vals, iter(v))
  #   return zip(it_keys, it_vals)

  # def reindex_keys(self, index_set: Iterable):
  #   ''' Given a totally ordered key set of the same length of the filtation, reindexes '''
  #   assert len(index_set) == len(self)
  #   assert all((i <= j for i,j in pairwise(index_set)))
  #   new = MutableFiltration(zip(iter(index_set), self.values()))
  #   return new

  # def faces(self, p: int = None) -> Iterable:
  #   return filter(lambda s: len(s) == p+1, self.values())

  # def __repr__(self) -> str:
  #   # from collections import Counter
  #   # cc = Counter([len(s)-1 for s in self.values()])
  #   # cc = dict(sorted(cc.items()))
  #   n = len(self.shape)
  #   return f"{n-1}-d filtered complex with {self.shape}-simplices of dimension {tuple(range(n))}"

  # def print(self, **kwargs) -> None:
  #   import sys
  #   fv_s, fs_s = [], []
  #   for k,v in self.items():
  #     ks = len(str(v))
  #     fv_s.append(f"{str(k):<{ks}.{ks}}")
  #     fs_s.append(f"{str(v): <{ks}}")
  #     assert len(fv_s[-1]) == len(fs_s[-1])
  #   sym_le, sym_inc = (' ≤ ', ' ⊆ ') if sys.getdefaultencoding()[:3] == 'utf' else (' <= ', ' <= ') 
  #   print(repr(self))
  #   print("I: " + sym_le.join(fv_s[:5]) + sym_le + ' ... ' + sym_le + sym_le.join(fv_s[-2:]), **kwargs)
  #   print("S: " + sym_inc.join(fs_s[:5]) + sym_inc + ' ... ' + sym_inc + sym_inc.join(fs_s[-2:]), **kwargs)

  # def validate(self, light: bool = True) -> bool:
  #   fs = list(self.values())
  #   for i, s in enumerate(fs): 
  #     p = s.dimension() - 1 if light and len(s) >= 2 else None
  #     assert all([fs.index(face) <= i for face in s.faces(p)])
  #   assert all([k1 <= k2 for k1, k2 in pairwise(self.keys())])

  # def __format__(self, format_spec = "default") -> str:
  #   from io import StringIO
  #   s = StringIO()
  #   self.print(file=s)
  #   res = s.getvalue()
  #   s.close()
  #   return res
  