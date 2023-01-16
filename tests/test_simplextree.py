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
  s.insert(vertices)
  assert s.vertices == [0, 1, 2, 3, 4, 5, 6, 8, 9]
  
  s = st.SimplexTree()
  simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  assert s.insert(simplex) is None 
  assert s.dimension == 4
  assert all(s.n_simplices == np.array([5,10,10,5,1]))

  s = SimplexTree()
  

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