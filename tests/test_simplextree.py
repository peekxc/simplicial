import numpy as np 

from simplicial.simplextree import st


def test_can_import():
  assert str(type(st)) == "<class 'module'>"
  assert "SimplexTree" in dir(st)
  assert str(type(st.SimplexTree)) == "<class 'pybind11_builtins.pybind11_type'>"


def test_construct():
  s = st.SimplexTree()
  simplices = np.array([[0,1,2], [1,2,3]], dtype=np.int8)
  s.insert(simplices)

  vertices = np.array([0,1,2,3,4,5,6], dtype=np.int8)
  s.insert(vertices)
  
  s.n_simplices

  s.is_tree()
  s.n_simplices
  s.find([0, 1])
  s.find(np.array([[1,2],[0,1]], dtype=np.int16))