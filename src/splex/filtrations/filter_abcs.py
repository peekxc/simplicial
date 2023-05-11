# from abc import ABC
from collections.abc import Set
import sys
from ..meta import * 
from ..generics import * 


class Filtration(Set, ComplexLike):
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
