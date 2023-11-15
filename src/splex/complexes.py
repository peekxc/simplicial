from typing import * 
from .meta import SimplexConvertible, SimplexLike
from .generics import dim, faces
from .complex_abcs import * 
from .RankComplex import RankComplex
from .SetComplex import SetComplex
from .Simplex import Simplex

def simplicial_complex(simplices: Iterable[SimplexConvertible] = None, form: str = "default"):
  """Abstract simplicial complex constructor.
  
  Parameters:
    simplices: Iterable of SimplexConvertible objects. 
    form: one of ['set', 'tree', 'rank']. Defaults to 'set'. 

  Returns:
    sc: a _ComplexLike_ structure whose structure depends on _form_.
  """ 
  if form is None or isinstance(form, str) and form == "default":
    form = "set"
  assert isinstance(form, str), f"Invalid form argument of type '{type(form)}'; must be string."
  form = form.strip().lower()
  if form == "tree":
    from simplextree import SimplexTree
    sc = SimplexTree(simplices)
  elif form == "rank":
    sc = RankComplex(simplices)
  elif form == "set":
    sc = SetComplex(simplices)
  else: 
    raise ValueError(f"Invalid form '{form}'.")
  return sc 

def print_complex(S: ComplexLike, **kwargs):
  assert is_complex_like(S), "Must a complex-like input."
  ST = np.zeros(shape=(len(S), dim(S)+1), dtype='<U15')
  ST.fill(' ')
  for i,s in enumerate(S):
    ST[i,:len(s)] = str(Simplex(s))[1:-1].split(',')
  SC = np.apply_along_axis(lambda x: ' '.join(x), axis=0, arr=ST)
  for i, s in enumerate(SC): 
    ending = '\n' if i != (len(SC)-1) else ''
    print(s, sep='', end=ending, **kwargs)
