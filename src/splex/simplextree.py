from __future__ import annotations
from typing import *
from numpy.typing import ArrayLike

import numpy as np 
import _simplextree
from _simplextree import SimplexTree as SimplexTreeCpp
from .splex import *

class SimplexTree(SimplexTreeCpp):
  """ 
  SimplexTree provides lightweight wrapper around a Simplex Tree data structure: an ordered, trie-like structure whose nodes are in bijection with the faces of the complex. 
  This class exposes a native extension module wrapping a simplex tree implemented with modern C++.

  The Simplex Tree was originally introduced in the following paper:

    Boissonnat, Jean-Daniel, and Clément Maria. "The simplex tree: An efficient data structure for general simplicial complexes." Algorithmica 70.3 (2014): 406-427.
  """    
  def __init__(self, simplices: Iterable[SimplexLike] = None) -> None:
    SimplexTreeCpp.__init__(self)
    if simplices is not None: 
      self.insert(simplices)
    return None

  def insert(self, simplices: Iterable[SimplexLike]) -> None:
    """
    Inserts simplices into the Simplex Tree. 

    Note inserting a simplex by definition also inserts all of its faces. If the simplex exists, the tree is not modified. 

    Parameters:
      simplices: Iterable of simplices to insert (each of which are SimplexLike)

    Note: 
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
    Computes the degree of select vertices in the trie.

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
  def traverse(order: str = "preorder", f: Callable = print, **kargs) -> None:
    """
    Parameters:
      order : the type of traversal to do 
      f : a function to evaluate on every simplex in the traversal. Defaults to print. 
      **kwargs : additional arguments to the specific traversal. 
    """
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
    self._traverse(3, lambda s: f(s), [], p) # order, f, init, k

  def cofaces(self, p: int = None, sigma: SimplexLike = []) -> list['SimplexLike']:
    """
    Parameters:
      p : coface dimension to restrict to 
      sigma : the simplex to obtain cofaces of

    
    Returns: 
      list: the p-cofaces of sigma
    """
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

  def expand(self, k: int) -> None:
    """ 
    Performs a k-expansion of the tree.
    
    Parameters: 
      k : maximum dimension to expand to. 
    """
    assert int(k) >= 0, f"Invalid expansion dimension k={k} given"
    self._expand(int(k))


  def __repr__(self) -> str:
    return f"Simplex Tree with {tuple(self.n_simplices)} {tuple(range(0,self.dimension+1))}-simplices"