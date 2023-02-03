# python -m pytest tests/
import numpy as np 

from simplicial.simplextree import _simplextree as st_mod
from simplicial.simplextree import SimplexTree

def test_can_import():
  assert str(type(st_mod)) == "<class 'module'>"
  assert "SimplexTree" in dir(st_mod)
  assert str(type(st_mod.SimplexTree)) == "<class 'pybind11_builtins.pybind11_type'>"

def test_construct():
  s = st_mod.SimplexTree()
  assert str(type(s)) == "<class '_simplextree.SimplexTree'>"
  s = SimplexTree()
  assert str(type(s)) == "<class 'simplicial.simplextree.SimplexTree'>"

def test_insert():
  st = SimplexTree()
  simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  assert st.insert(simplex) is None 
  assert st.dimension == 4
  assert all(st.n_simplices == np.array([5,10,10,5,1]))

def test_expand():
  from itertools import combinations
  st = SimplexTree()
  simplex = np.array([0,1,2,3,4], dtype=np.int8)
  st.insert([(i,j) for i,j in combinations(simplex, 2)])
  st.expand(k=1)
  assert all(st.n_simplices == np.array([5,10]))
  st.expand(k=2)
  assert all(st.n_simplices == np.array([5,10,10]))
  st.expand(k=5)
  assert all(st.n_simplices == np.array([5,10,10,5,1]))
  assert st.insert([simplex]) is None 
  assert all(st.n_simplices == np.array([5,10,10,5,1]))
  assert st.dimension == 4


def test_SimplexTree():
  st = SimplexTree()
  st.insert([[0,1,2], [0,1], [4,5]])

  # t order, py::function f, simplex_t init = simplex_t(), const size_t k = 0
  # stree._traverse(0, lambda s: print(Simplex(s)), [], 0)
  # stree._traverse(1, lambda s: print(s), [], 0)
  # stree._traverse(2, lambda s: print(s), [1,2,3], 0)
  
  # stree._traverse(7, lambda s: yield s, [], 0) ## maximal
  ## Everything works! Now to wrap up with straverse, ltraverse, generators from orders, wrappers, ....


def test_remove():
  assert True
  # s = st.SimplexTree()
  # simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  # assert s.insert(simplex) is None 
 
  
  # s.vertices
  # s.n_simplices

  # s.is_tree()
  # s.n_simplices
  # s.find([0, 1])
  # s.find(np.array([[1,2],[0,1]], dtype=np.int16))