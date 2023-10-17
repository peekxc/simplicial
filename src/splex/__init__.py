## __init__.py 
## initialization module for simplicial package 
# from .meta import SimplexLike, ComplexLike, FiltrationLike
# from .splex import SimplicialComplex, MutableFiltration
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

## Temporary for dev 
from .meta import *
from .generics import *
from .complexes import *
from .filtrations import *
from .sparse import *
from .geometry import *
