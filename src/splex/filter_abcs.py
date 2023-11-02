# from abc import ABC
import abc
from collections.abc import Set
from typing import *
import sys
import operator
from more_itertools import nth
from .meta import * 
from .generics import * 
from .Simplex import Simplex, ValueSimplex

class Filtration(ComplexLike):
  """Simplex-wise filtration ABC."""

  ## ---- Collection requirements -----
  @abstractmethod
  def __iter__(self) -> tuple[Any, SimplexConvertible]: 
    pass 

  @abstractmethod
  def __len__(self) -> int:
    pass 

  @abstractmethod
  def __contains__(self, k: SimplexConvertible) -> bool:
    pass 

  ## --- Set requirements ---
  def __eq__(self, other) -> bool:
    if len(self) != len(other): 
      return False 
    else: 
      return all(k1 == k2 and v1 == v2 for (k1,v1), (k2,v2) in zip(iter(self), iter(other)))

  ## --- Sequence requirements ---
  def __getitem__(self, key: int) -> SimplexConvertible: 
    if len(self) <= key: 
      raise IndexError("index out of range")
    return nth(iter(self), key, None)

  def index(self, item: SimplexConvertible) -> int:  
    s = Simplex(item)
    for i,x in iter(self):
      if x == s:
        return i
    return -1  

  def count(self, item: SimplexConvertible) -> int: 
    s = Simplex(item)
    s_count = 0
    for i,x in iter(s):
      s_count += (x == s)
    return s_count
  
  ## --- Disable Mutable Sequence ---- 
  def __setitem__(self, key: Any, value: Any):
    raise TypeError("Object does not support item assignment")
  
  def __delitem__(self, key: Any) -> None:
    if hasattr(self, 'discard'):
      self.discard(key)
    else:
      raise TypeError("Object does not support item deletion")
    
  def insert(self, index: int, object: Any):
    raise TypeError("Filtrations do not support insertions at an index. Use 'add' instead.")

  ## --- splex generics support --- 
  def dim(self) -> int:
    return max(len(s) - 1 for k,s in iter(self))

  def faces(self, p: int = None, **kwargs) -> Iterator[ValueSimplex]:
    assert isinstance(p, Integral) or p is None, f"Invalid p:{p} given"
    simplices_map = map(operator.itemgetter(1), iter(self))
    if p is None:
      return iter(simplices_map)
    else:
      return filter(lambda s: len(s) == p+1, iter(simplices_map))
    
  def indices(self) -> Iterator[Any]:
    return iter(map(operator.itemgetter(0), iter(self)))

  ## --- Misc utilities ---
  def __format__(self, format_spec = "default") -> str:
    from io import StringIO
    s = StringIO()
    self.print(file=s)
    res = s.getvalue()
    s.close()
    return res

  def __repr__(self) -> str:
    if len(self) == 0:
      return f"Empty filtration"
    d = dim(self)
    return f"{d}-d filtered complex with {card(self)}-simplices of dimension {tuple(range(d+1))}"

  def print(self, **kwargs) -> None:
    fv_s, fs_s = [], []
    for k, v in iter(self):
      ks = len(str(v))
      fv_s.append(f"{str(k):<{ks}.{ks}}")
      fs_s.append(f"{str(v): <{ks}}")
      assert len(fv_s[-1]) == len(fs_s[-1])
    sym_le, sym_inc = (' ≤ ', ' ⊆ ') if sys.getdefaultencoding()[:3] == 'utf' else (' <= ', ' <= ') 
    print(repr(self), **kwargs)
    print("I: " + sym_le.join(fv_s[:5]) + sym_le + ' ... ' + sym_le + sym_le.join(fv_s[-2:]), **kwargs)
    print("S: " + sym_inc.join(fs_s[:5]) + sym_inc + ' ... ' + sym_inc + sym_inc.join(fs_s[-2:]), **kwargs)

class MutableFiltration(Filtration):
  ## --- MutableSet requirements ---
  @abstractmethod
  def add(self, simplex: SimplexConvertible) -> None:
    pass

  @abstractmethod 
  def discard(self, simplex: SimplexConvertible):
    pass