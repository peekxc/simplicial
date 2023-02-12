from ..meta import * 
from .RankComplex import RankComplex
from .SimplexTree import SimplexTree
from .SetComplex import SetComplex

def simplicial_complex(simplices: Iterable[SimplexConvertible] = None, form: str = "default"):
  """Wrapper for constructing an abstract simplicial complex.
  
  Parameters:
    simplices = Iterable of SimplexConvertible objects. 
    form = one of ['set', 'tree', 'rank']. Defaults to 'set'. 

  Returns:
    sc = a _ComplexLike_ structure whose structure depends on _form_.
  """ 
  if form is None or isinstance(form, str) and form == "default":
    form = "set"
  assert isinstance(form, str), f"Invalid form argument of type '{type(form)}'; must be string."
  form = form.strip().lower()
  if form == "tree":
    sc = SimplexTree(simplices)
  elif form == "rank":
    sc = RankComplex(simplices)
  elif form == "set":
    sc = SetComplex(simplices)
  else: 
    raise ValueError(f"Invalid form '{form}'.")
  return sc 

