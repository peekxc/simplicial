import numpy as np
from scipy.spatial.distance import pdist

from .splex import * 
from .simplextree import * 
from .combinatorial import rank_combs, unrank_combs


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
      return pd[int(rank_combs([s], n=n, order='lex')[0])]
    else: 
      return max(pd[np.array(rank_combs(s.faces(1), n=X.shape[0], order='lex'), dtype=int)])
  simplices = list(map(Simplex, st.simplices()))
  filter_weights = np.array([_clique_weight(s) for s in simplices])
  K = MutableFiltration(zip(filter_weights, simplices))
  return K




