import numpy as np 
from typing import *
from numpy.typing import ArrayLike
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

  def insert(self, simplices: Iterable):
    ## TODO: figure out to interface to underlying st object
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

  def collapse(self, sigma, tau):
    pass 

  def degree(self, vertices: Optional[ArrayLike] = None) -> Union[ArrayLike, int]:
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
  def traverse(order: str = "preorder"):
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

  def cofaces(p: int = None, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(3, lambda s: F.append(s), [], p) # order, f, init, k
    return F

  def skeleton(p: int = None) -> Iterable['SimplexLike']:
    F = []
    self._traverse(5, lambda s: F.append(s), sigma, self.dimension)
    return F 

  def simplices(p: int = None, sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(6, lambda s: F.append(s), [], p) # order, f, init, k
    return F
  
  def maximal() -> Iterable['SimplexLike']:
    F = []
    self._traverse(7, lambda s: F.append(s), p)
    return F

  def link(sigma: SimplexLike = []) -> Iterable['SimplexLike']:
    F = []
    self._traverse(8, lambda s: F.append(s), sigma, 0)
    return F

