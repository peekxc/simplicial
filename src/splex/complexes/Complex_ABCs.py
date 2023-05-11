from collections.abc import Set
import sys
from ..meta import * 
from ..generics import * 

class Complex(Set, ComplexLike):
  def __repr__(self) -> str:
    if len(self) == 0:
      return f"Empty complex"
    from collections import Counter
    cc = Counter([dim(s) for s in iter(self)])
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
