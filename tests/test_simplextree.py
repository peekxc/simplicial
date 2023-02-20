# python -m pytest tests/
import numpy as np 
from splex.complexes import SimplexTree

def test_construct():
  s = SimplexTree()
  assert str(type(s)) == "<class 'splex.complexes.SimplexTree.SimplexTree'>"
  st = SimplexTree([[0,1,2,3,4]])
  assert all(st.n_simplices == np.array([5,10,10,5,1]))

## Minimal API tests
def test_SimplexTree():
  st = SimplexTree()
  st.insert([[0,1,2], [0,1], [4,5], [1,4], [1,5]])
  assert all(st.n_simplices == np.array([5,6,1]))
  st.traverse("preorder", print, [], 0)
  st.traverse("preorder", print, [0,1], 1)
  st.traverse("level_order", print, [], 0)
  st.traverse("k_simplices", print, [], 0)
  st.traverse("k_skeleton", print, [], 1)
  st.traverse("cofaces", print, [0], 0)
  # st.traverse("maximal", print, [0], 1)


  st.simplices()
  st.maximal()


def test_insert():
  st = SimplexTree()
  simplex = np.array([[0,1,2,3,4]], dtype=np.int8)
  assert st.insert(simplex) is None 
  assert st.dimension == 4
  assert all(st.n_simplices == np.array([5,10,10,5,1]))

def test_traverse():
  st = SimplexTree([[0,1,2,3,4]])
  st.traverse

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


  # t order, py::function f, simplex_t init = simplex_t(), const size_t k = 0
  # stree._traverse(0, lambda s: print(Simplex(s)), [], 0)
  # stree._traverse(1, lambda s: print(s), [], 0)
  # stree._traverse(2, lambda s: print(s), [1,2,3], 0)
  
  # stree._traverse(7, lambda s: yield s, [], 0) ## maximal
  ## Everything works! Now to wrap up with straverse, ltraverse, generators from orders, wrappers, ....


def test_remove():
  st = SimplexTree([[0,1,2,3,4]])
  st.remove([[0,1,2]])
  assert all(st.n_simplices == np.array([5,10,9,3]))
  assert all(st.find([[0,1], [1,2], [0,1,2]]) == np.array([True, True, False]))