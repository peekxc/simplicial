import numpy as np

from .meta import *
from .generics import * 
from .splex import * 
from .simplextree import * 
from .combinatorial import rank_combs, unrank_combs
from scipy.spatial.distance import pdist

def rips_filtration(X: ArrayLike, radius: float) -> MutableFiltration:
  X = np.random.uniform(size=(30,2))
  pd = pdist(X)
  ind = np.flatnonzero(pd <= 2*radius)
  
  st = SimplexTree(unrank_combs(ind, n=X.shape[0], k=2))
  st.expand(2)
  n = X.shape[0]
  def _clique_weight(s: SimplexLike) -> float:
    if len(s) == 1:
      return 0
    elif len(s) == 2:
      return pd[int(rank_combs([s], k=2, n=n))]
    else: 
      return max(pd[rank_combs(s.faces(1), n=X.shape[0], k=2)])
  MutableFiltration(st, )




