import numpy as np 

from simplicial.simplextree import st
from simplicial.simplextree import SimplexTree

def test_can_import():
  assert str(type(st)) == "<class 'module'>"
  assert "SimplexTree" in dir(st)
  assert str(type(st.SimplexTree)) == "<class 'pybind11_builtins.pybind11_type'>"

def test_construct():
  s = st.SimplexTree()
  assert str(type(s)) == "<class '_simplextree.SimplexTree'>"
  s = SimplexTree()
  assert str(type(s)) == "<class 'simplicial.simplextree.SimplexTree'>"

def test_insert():
  s = st.SimplexTree()
  vertices = np.array([0,1,2,3,4,5,6,8,9], dtype=np.int8)
  s._insert(vertices)
  assert s.vertices == [0, 1, 2, 3, 4, 5, 6, 8, 9]
  
  s = st.SimplexTree()
  simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  assert s._insert(simplex) is None 
  assert s.dimension == 4
  assert all(s.n_simplices == np.array([5,10,10,5,1]))


def test_SimplexTree():
  stree = SimplexTree()
  stree.insert([[0,1,2,3,4,5]])
  stree.n_simplices
  # t order, py::function f, simplex_t init = simplex_t(), const size_t k = 0
  stree._traverse(0, lambda s: print(Simplex(s)), [], 0)
  stree._traverse(1, lambda s: print(s), [], 0)
  stree._traverse(2, lambda s: print(s), [1,2,3], 0)
  
  # stree._traverse(7, lambda s: yield s, [], 0) ## maximal
  ## Everything works! Now to wrap up with straverse, ltraverse, generators from orders, wrappers, ....

  stree._traverse

def test_remove():
  s = st.SimplexTree()
  simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  assert s.insert(simplex) is None 
 
  
  s.vertices
  s.n_simplices

  s.is_tree()
  s.n_simplices
  s.find([0, 1])
  s.find(np.array([[1,2],[0,1]], dtype=np.int16))