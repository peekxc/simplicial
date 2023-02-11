## splex.py
## Contains definitions and utilities for prescribing a structural type system on the 
## space of abstract simplicial complexes and on simplicial filtrations
import numpy as np   
from scipy.sparse import coo_array
from .generics import *   

@dataclass(frozen=True)
class Simplex(Set, Hashable):
  '''Dataclass for representing a simplex. 

  A simplex is a value type object supporting set-like behavior. Simplex instances are hashable, comparable, immutable, and homogenous. 
  
  This class is also SimplexLike.
  
  Magics:
    __hash__  
    __contains__(self, v: int) <=> Returns whether integer 'v' is a vertex in 'self'
  '''
  # __slots__ = 'vertices'
  vertices: tuple = ()
  def __init__(self, v: Collection[Integral]) -> None:
    t = tuple([int(v)]) if isinstance(v, Number) else tuple(np.unique(np.sort(np.ravel(tuple(v)))))
    object.__setattr__(self, 'vertices', t)
    assert all([isinstance(v, Integral) for v in self.vertices]), "Simplex must be comprised of integral types."
  def __eq__(self, other) -> bool: 
    if len(self) != len(other):
      return False
    return(all(v == w for (v,w) in zip(iter(self.vertices), iter(other))))
  def __len__(self):
    return len(self.vertices)
  def __lt__(self, other: Collection[int]) -> bool:
    if len(self) >= len(other): 
      return(False)
    else:
      return(all([v in other for v in self.vertices]))
  def __le__(self, other: Collection) -> bool: 
    if len(self) > len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self < other
  def __ge__(self, other: Collection[int]) -> bool:
    if len(self) < len(other): 
      return(False)
    elif len(self) == len(other):
      return self.__eq__(other)
    else:
      return self > other
  def __gt__(self, other: Collection[int]) -> bool:
    if len(self) <= len(other): 
      return(False)
    else:
      return(all([v in self.vertices for v in other]))
  def __contains__(self, __x: int) -> bool:
    """ Reports vertex-wise inclusion """
    if not isinstance(__x, Number): 
      return False
    return self.vertices.__contains__(__x)
  
  def __iter__(self) -> Iterable[int]:
    return iter(self.vertices)
  def __repr__(self):
    return str(self.vertices).replace(',','') if self.dim() == 0 else str(self.vertices).replace(' ','')
  def __getitem__(self, index: int) -> int:
    return self.vertices[index] # auto handles IndexError exception 
  def __sub__(self, other) -> 'Simplex':
    return Simplex(set(self.vertices) - set(Simplex(other).vertices))
  def __add__(self, other) -> 'Simplex':
    return Simplex(set(self.vertices) | set(Simplex(other).vertices))
  def __hash__(self) -> int:
    # Because Python has no idea about mutability of an object.
    return hash(self.vertices)

  def faces(self, p: Optional[int] = None) -> Iterable['Simplex']:
    dim = len(self.vertices)
    if p is None:
      yield from map(Simplex, chain(*[combinations(self.vertices, d) for d in range(1, dim+1)]))
    else: 
      yield from filter(lambda s: len(s) == p+1, self.faces(None))

  def boundary(self) -> Iterable['Simplex']: 
    if len(self.vertices) == 0: 
      return self.vertices
    yield from map(Simplex, combinations(self.vertices, len(self.vertices)-1))

  def dim(self) -> int: 
    return len(self.vertices)-1
    


## TODO: implement a simplex |-> attribute system like networkx graphs
# https://stackoverflow.com/questions/798442/what-is-the-correct-or-best-way-to-subclass-the-python-set-class-adding-a-new
class SimplicialComplex(MutableSet, ComplexLike):
  """ Abstract Simplicial Complex"""
  __hash__ = Set._hash

  def __init__(self, simplices: Iterable[SimplexLike] = None):
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

# MutableMapping abc 
# Requires: __getitem__, __delitem__, __setitem__ , __iter__, and __len__ a
# Inferred: pop, clear, update, and setdefault
# https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/
class MutableFiltration(MutableMapping):
  """
  Simplicial Filtration 

  Implements: __getitem__, __iter__, __len__, __contains__, keys, items, values, get, __eq__, and __ne__
  """

  @classmethod
  def _key_dim_lex_poset(cls, s: Simplex) -> bool:
    return (len(s), tuple(s), s)

  ## Returns a newly allocated Sorted Set w/ lexicographical poset ordering
  def _sorted_set(self, iterable: Iterable[Collection[Integral]] = None) -> SortedSet:
    key = MutableFiltration._key_dim_lex_poset
    return SortedSet(None, key) if iterable is None else SortedSet(iter(map(Simplex, iterable)), key)
  
  # simplices: Sequence[SimplexLike], I: Optional[Collection] = None
  # Accept: 
  # x simplices_iterable, f = None (this shouldnt work)
  # simplices_iterable, f = Callable
  # (index_iterable, simplices_iterable)
  # SimplicialComplex, f = None 
  # SimplicialComplex, f = Callable 
  def __init__(self, simplices: Union[SimplicialComplex, Iterable] = None, f: Optional[Callable] = None) -> None:
    self.data = SortedDict()
    self.shape = tuple()
    if isinstance(simplices, SimplicialComplex):
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
    self.data.__del__(k)
  
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
  def copy(self) -> 'MutableFiltration':
    new = MutableFiltration()
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
      new = MutableFiltration(zip(iter(index_set), self.values()))
      self.data = new.data
    elif isinstance(index_set, Callable):
      new = MutableFiltration(simplices=self.values(), f=index_set)
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
    print(repr(self))
    print("I: " + sym_le.join(fv_s[:5]) + sym_le + ' ... ' + sym_le + sym_le.join(fv_s[-2:]), **kwargs)
    print("S: " + sym_inc.join(fs_s[:5]) + sym_inc + ' ... ' + sym_inc + sym_inc.join(fs_s[-2:]), **kwargs)

  def validate(self, light: bool = True) -> bool:
    fs = list(self.values())
    for i, s in enumerate(fs): 
      p = s.dimension() - 1 if light and len(s) >= 2 else None
      assert all([fs.index(face) <= i for face in s.faces(p)])
    assert all([k1 <= k2 for k1, k2 in pairwise(self.keys())])

  def __format__(self, format_spec = "default") -> str:
    from io import StringIO
    s = StringIO()
    self.print(file=s)
    res = s.getvalue()
    s.close()
    return res


# See: https://stackoverflow.com/questions/70381559/ensure-that-an-argument-can-be-iterated-twice
def _boundary(S: Iterable[SimplexLike], F: Optional[Sequence[SimplexLike]] = None):

  ## Load faces. If not given, by definition, the given p-simplices contain their boundary faces.
  if F is None: 
    assert not(S is iter(S)), "Simplex iterable must be repeatable (a generator is not sufficient!)"
    F = list(map(Simplex, set(chain.from_iterable([combinations(s, len(s)-1) for s in S]))))
  
  ## Ensure faces 'F' is indexable
  assert isinstance(F, Sequence), "Faces must be a valid Sequence (supporting .index(*) with SimplexLike objects!)"

  ## Build the boundary matrix from the sequence
  m = 0
  I,J,X = [],[],[] # row, col, data 
  for (j,s) in enumerate(map(Simplex, S)):
    if dim(s) > 0:
      I.extend([F.index(f) for f in s.faces(dim(s)-1)])
      J.extend(repeat(j, dim(s)+1))
      X.extend(islice(cycle([1,-1]), dim(s)+1))
    m += 1
  D = coo_array((X, (I,J)), shape=(len(F), m)).tolil(copy=False)
  return D 

## TODO: investigate whether to make a 'ChainLike' for extension with 'BoundaryChain'
## something like chain(s: SimplexLike, c: ComplexLike, oriented: bool) -> ndarray, or generator (index, value)
## complexLike could be overloaded to handle .index(), checked if Sequence[SimplexLike] or if just Container[int] (+implying)
def boundary_matrix(K: Union[SimplicialComplex, MutableFiltration], p: Optional[Union[int, tuple]] = None):
  """
  Constructs a sparse boundary matrix of a given simplicial object _K_

  Returns: 
    D := sparse matrix representing either the full or p-th boundary matrix (as List-of-Lists format)
  """
  from collections.abc import Sized
  if isinstance(p, tuple):
    return (boundary_matrix(K, pi) for pi in p)
  else: 
    assert p is None or isinstance(p, Integral), "p must be integer, or None"
    if isinstance(K, SimplicialComplex) or isinstance(K, MutableFiltration):
      if p is None:
        simplices = list(K.faces())
        D = _boundary(simplices, simplices)
      else:
        p_simplices = K.faces(p=p)
        p_faces = list(K.faces(p=p-1))
        D = _boundary(p_simplices, p_faces)
    else: 
      raise ValueError("Invalid input")
    return D

