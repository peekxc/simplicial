import numbers
import numpy as np 
from typing import *
from numpy.typing import ArrayLike 
from more_itertools import spy

from .combinatorial import * 
from .meta import *

def is_simplex_like(x: Any) -> bool:
	return isinstance(x, SimplexConvertible) # is a Collection supporting __contains__, __iter__, and __len__

def is_complex_like(x: Any) -> bool: 
	if isinstance(x, ComplexLike): # is iterable
		item, iterable = spy(x)
		return is_simplex_like(item)
	return False

def is_filtration_like(x: Any) -> bool:
	return isinstance(x, FiltrationLike) and is_complex_like(x)

def is_array_convertible(x: Any) -> bool:
	return hasattr(x, "__array__")

def is_repeatable(x: Iterable) -> bool:
  return not(iter(x) is x)

def is_distance_matrix(x: ArrayLike) -> bool:
	"""Checks whether 'x' is a distance matrix, i.e. is square, symmetric, and that the diagonal is all 0."""
	x = np.array(x, copy=False)
	is_square = x.ndim == 2	and (x.shape[0] == x.shape[1])
	return(False if not(is_square) else np.all(np.diag(x) == 0))

def is_pairwise_distances(x: ArrayLike) -> bool:
	"""Checks whether 'x' is a 1-d array of pairwise distances."""
	x = np.array(x, copy=False) # don't use asanyarray here
	if x.ndim > 1: return(False)
	n = inverse_choose(len(x), 2)
	return(x.ndim == 1 and n == int(n))

def is_point_cloud(x: ArrayLike) -> bool: 
	"""Checks whether 'x' is a 2-d array of points"""
	return(isinstance(x, np.ndarray) and x.ndim == 2)

def is_dist_like(x: ArrayLike):
	"""Checks whether _x_ is any recognizable distance object."""
	return(is_distance_matrix(x) or is_pairwise_distances(x))