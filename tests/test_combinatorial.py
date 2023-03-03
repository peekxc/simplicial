import numpy as np
from splex.combinatorial import *
from itertools import combinations

def test_colex():
  n, k = 10, 3
  ranks = np.array([rank_colex(c) for c in combinations(range(n), k)])
  assert all(np.sort(ranks) == np.arange(comb(n,k))), "Colex ranking is not unique / does not form bijection"
  ranks2 = np.array([rank_colex(reversed(c)) for c in combinations(range(n), k)])
  assert all(ranks == ranks2), "Ranking is not order-invariant"
  combs_test = np.array([unrank_colex(r, k) for r in ranks])
  combs_truth = np.array(list(combinations(range(n),k)))
  assert all((combs_test == combs_truth).flatten()), "Colex unranking invalid"

def test_lex():
  n, k = 10, 3
  ranks = np.array([rank_lex(c, n) for c in combinations(range(n), k)])
  assert all(ranks == np.arange(comb(n,k))), "Lex ranking is not unique / does not form bijection"
  ranks2 = np.array([rank_lex(reversed(c), n) for c in combinations(range(n), k)])
  assert all(ranks == ranks2), "Ranking is not order-invariant"
  combs_test = np.array([unrank_lex(r, k, n) for r in ranks])
  combs_truth = np.array(list(combinations(range(n),k)))
  assert all((combs_test == combs_truth).flatten()), "Lex unranking invalid"

def test_api():
  n = 20
  for d in range(1, 5):
    combs = list(combinations(range(n), d))
    C = unrank_combs(rank_combs(combs), k=d)
    assert all([tuple(s) == tuple(c) for s,c in zip(combs, C)])
