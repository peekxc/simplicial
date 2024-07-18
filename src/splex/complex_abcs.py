import numpy as np
from collections.abc import Set
from io import StringIO
from .meta import ComplexLike
from .Simplex import Simplex

class Complex(Set, ComplexLike):
  def __format__(self, format_spec = "default") -> str:
    s = StringIO()
    self.print(file=s)
    res = s.getvalue()
    s.close()
    return res

  def print(self, **kwargs) -> None:
    ST = np.zeros(shape=(self.__len__(), self.dim()+1), dtype='<U15')
    ST.fill(' ')
    for i,s in enumerate(self):
      ST[i,:len(s)] = str(Simplex(s))[1:-1].split(',')
    SC = np.apply_along_axis(lambda x: ' '.join(x), axis=0, arr=ST)
    for i, s in enumerate(SC): 
      ending = '\n' if i != (len(SC)-1) else ''
      print(s, sep='', end=ending, **kwargs)
