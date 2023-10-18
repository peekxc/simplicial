# from abc import ABC
import abc
from collections.abc import Set
from typing import *
import sys
from more_itertools import nth
from ..meta import * 
from ..generics import * 
from ..Simplex import Simplex

class Filtration(ComplexLike):

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
    for v in faces(self):
      k = v.value
      ks = len(str(v))
      fv_s.append(f"{str(k):<{ks}.{ks}}")
      fs_s.append(f"{str(v): <{ks}}")
      assert len(fv_s[-1]) == len(fs_s[-1])
    sym_le, sym_inc = (' ≤ ', ' ⊆ ') if sys.getdefaultencoding()[:3] == 'utf' else (' <= ', ' <= ') 
    print(repr(self), **kwargs)
    print("I: " + sym_le.join(fv_s[:5]) + sym_le + ' ... ' + sym_le + sym_le.join(fv_s[-2:]), **kwargs)
    print("S: " + sym_inc.join(fs_s[:5]) + sym_inc + ' ... ' + sym_inc + sym_inc.join(fs_s[-2:]), **kwargs)
