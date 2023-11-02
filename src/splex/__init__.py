## __init__.py 
## initialization module for simplicial package 
# from .meta import SimplexLike, ComplexLike, FiltrationLike
# from .splex import SimplicialComplex, MutableFiltration
# import os, sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

## Primary names to export
from .meta import SimplexConvertible, SimplexLike, ComplexLike, FiltrationLike, PropertySimplexConvertible
from .generics import card, dim, faces, boundary
from .Simplex import Simplex, ValueSimplex, PropertySimplex
from .predicates import *
from .filters import fixed_filter, generic_filter, lower_star_filter, flag_filter
from .sparse import boundary_matrix
from .geometry import enclosing_radius, rips_complex, rips_filtration, delaunay_complex
from .complexes import SetComplex, RankComplex, simplicial_complex
from .filtrations import SetFiltration, RankFiltration, filtration

## Modules to expose
## Since Python has such terrible support for simple relative imports, we put everything in one directory
# from . import complexes
# from . import filtrations

# __all__ = [ComplexLike, ]

