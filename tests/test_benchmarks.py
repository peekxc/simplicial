import numpy as np 
from splex import Simplex


def test_simplex_bench(benchmark):
  benchmark([Simplex(np.random.choice(range(10), size=8)) for i in range(1000)])
  assert True
  
    