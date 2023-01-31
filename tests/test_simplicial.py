import numpy as np 
from simplicial.simplicial import * 


def test_simplex():
  s = Simplex([0,1,2])
  assert isinstance(s, Simplex)
  assert isinstance(s, SimplexLike)