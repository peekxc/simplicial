from __future__ import annotations
from typing import *
from numpy.typing import ArrayLike

import numpy as np 
import _simplextree
from _simplextree import SimplexTree as SimplexTreeCpp
from .simplicial import *

class SimplexTree(SimplexTreeCpp):
  """ 
  Simplex Tree class 
  """    
  def __init__(self):
    SimplexTreeCpp.__init__(self)
    pass 

  def insert(self, simplices: Iterable[SimplexLike]) -> None:
    """
    Parameters:
      simplices: Inserts simplices into the simplex tree 
        If the iterable is an 2-dim np.ndarray, then a p-simplex is inserted along each contiguous p+1 stride.
        Otherwise, each element of the iterable to casted to a Simplex and then inserted into the tree. 
    """
    if isinstance(simplices, np.ndarray):
      simplices = np.array(simplices, dtype=np.int8)
      assert simplices.ndim in [1,2], "dimensions should be 1 or 2"
      self._insert(simplices)
    elif isinstance(simplices, Iterable): 
      simplices = [Simplex(s) for s in simplices]
      self._insert_list(simplices)
    else: 
      raise ValueError("Invalid type given")
  
  def remove(self, simplices: Iterable):
    pass 

  def find(self, simplices: Iterable):
    pass 

  def adjacent(self, simplices: Iterable):
    pass

  def collapse(self, sigma: SimplexLike, tau: SimplexLike):
    pass 

  def degree(self, vertices: Optional[ArrayLike] = None) -> Union[ArrayLike, int]:
    """
    Parameters:
      vertices (ArrayLike): Retrieves vertex degrees
        If no vertices are specified, all degrees are computed. Non-existing vertices by default have degree 0. 
    
    Returns: 
      list: degree of each vertex id given in 'vertices'
    """
    if vertices is None: 
      return self._degree_default()
    elif isinstance(vertices, Iterable): 
      vertices = np.fromiter(iter(vertices), dtype=np.int8)
      assert vertices.ndim == 1, "Invalid shape given; Must be flattened array of vertex ids"
      self._degree(vertices)
    else: 
      raise ValueError(f"Invalid type {type(vertices)} given")

  # PREORDER = 0, LEVEL_ORDER = 1, FACES = 2, COFACES = 3, COFACE_ROOTS = 4, 
  # K_SKELETON = 5, K_SIMPLICES = 6, MAXIMAL = 7, LINK = 8
  def traverse(order: str = "preorder", f: Callable[SimplexLike, Any] = print, **kargs):
    # todo: handle kwargs
    assert isinstance(order, str)
    order = order.lower() 
    if order in ["dfs", "preorder"]:
      order = 0
    elif order in ["bfs", "level_order", "levelorder"]:
      order = 1
    elif order == "faces":
      order = 2
    elif order == "cofaces":
      order = 3
    elif order == "coface_roots":
      order = 4
    elif order == "k_skeleton":
      order = 5
    elif order == "k_simplices":
      order = 6
    elif order == "maximal":
      order = 7
    elif order == "link":
      order = 8
    else: 
      raise ValueError(f"Unknown order '{order}' specified")
    self._traverse(3, lambda s: F.append(s), [], p) # order, f, init, k

  def cofaces(self, p: int = None, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(3, lambda s: F.append(s), [], p) # order, f, init, k
    return F
  
  def coface_roots(self, p: int = None, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(4, lambda s: F.append(s), [], p) # order, f, init, k
    return F

  def skeleton(self, p: int = None) -> Iterable['SimplexLike']:
    F = []
    self._traverse(5, lambda s: F.append(s), sigma, self.dimension)
    return F 

  def simplices(self, p: int = None, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(6, lambda s: F.append(s), [], p) # order, f, init, k
    return F
  
  def maximal(self) -> Iterable['SimplexLike']:
    F = []
    self._traverse(7, lambda s: F.append(s), p)
    return F

  def link(self, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(8, lambda s: F.append(s), sigma, 0)
    return F

  def __repr__(self) -> str:
    return f"Simplex Tree with {tuple(self.n_simplices)} {tuple(range(0,st.dimension+1))}-simplices"