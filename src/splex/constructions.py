import numpy as np
from scipy.spatial.distance import pdist, squareform

from .splex import * 
from .simplextree import * 
from .combinatorial import rank_combs, unrank_combs

def enclosing_radius(a: ArrayLike) -> float:
	''' Returns the smallest 'r' such that the Rips complex on the union of balls of radius 'r' is contractible to a point. '''
	# assert is_distance_matrix(a)
	return(np.min(np.amax(a, axis = 0)))

def rips_filtration(X: ArrayLike, radius: float = None) -> MutableFiltration:
  #X = np.random.uniform(size=(30,2))
  pd = pdist(X)
  radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  st = SimplexTree(unrank_combs(ind, n=X.shape[0], k=2, order="lex"))
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




