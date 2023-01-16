
from typing import *
import _simplextree as st
from _simplextree import SimplexTree as SimplexTreeCpp

class SimplexTree(SimplexTreeCpp):
  def __init__(self):
    SimplexTreeCpp.__init__(self)
    pass 
  def insert(simplices: Iterable):
    ## TODO: figure out to interface to underlying st object
    simplices = np.array(simplices, dtype=np.int8)



