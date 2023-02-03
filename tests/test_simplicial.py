import numpy as np 
from splex import * 


def test_simplex():
  s = Simplex([0,1,2])
  assert isinstance(s, Simplex)
  assert isinstance(s, SimplexLike)

def test_combinatorial_complex():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)
  
def test_combinatorial_filtration():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)
  K = CombinatorialFiltration(S)