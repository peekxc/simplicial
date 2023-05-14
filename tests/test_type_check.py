import numpy as np 
from typing import * 
from itertools import combinations
from numbers import Integral
from splex import * 

def test_predicates():
  s = Simplex([0,1,2])
  S = simplicial_complex([[0,1,2]])
  K = filtration(enumerate(S))
  
