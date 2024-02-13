import numbers
import numpy as np 
from typing import *
from numpy.typing import ArrayLike 
from more_itertools import spy
from operator import itemgetter

from .meta import *
from math import comb, factorial
# from .combinatorial import * 

def is_repeatable(x: Iterable) -> bool:
	"""Checks whether _x_ is Iterable and repeateable as an Iterable (generators fail this test)."""
	return not(iter(x) is x)

def is_simplex_like(x: Any) -> bool:
	"""An object 'x' is simplex like if it is a container of integral-types."""
	is_collection = isinstance(x, SimplexConvertible) # is a Collection supporting __contains__, __iter__, and __len__
	if is_collection: 
		return is_repeatable(x) and all([isinstance(v, Integral) for v in x])
	return False

def is_complex_like(x: Any) -> bool: 
	"""An object 'x' is complex like if it is iterable, sized, and it's first element is simplex like."""
	if isinstance(x, ComplexLike): # is iterable + Sized 
		(item,), iterable = spy(x, 1)
		return is_simplex_like(item)
	return False

def is_filtration_like(x: Any) -> bool:
	is_collection = isinstance(x, FiltrationLike) # Collection + Sequence + .index 
	if is_collection:
		# return is_complex_like(map(itemgetter(1), x))
		item, iterable = spy(x)
		return len(item[0]) == 2 and is_simplex_like(item[0][1])
	return False

def is_array_convertible(x: Any) -> bool:
	return hasattr(x, "__array__")

def is_distance_matrix(x: ArrayLike) -> bool:
	"""Checks whether _x_ is a distance matrix, i.e. is square, symmetric, and that the diagonal is all 0."""
	x = np.array(x, copy=False)
	is_square = x.ndim == 2	and (x.shape[0] == x.shape[1])
	return(False if not(is_square) else np.all(np.diag(x) == 0))

def is_pairwise_distances(x: ArrayLike) -> bool:
	"""Checks whether 'x' is a 1-d array of pairwise distances."""
	x = np.array(x, copy=False) # don't use asanyarray here
	if x.ndim > 1: return(False)
	N = len(x)
	rng = np.arange(np.floor(np.sqrt(2*N)), np.ceil(np.sqrt(2*N)+2) + 1, dtype=np.uint64)
	n = rng[np.searchsorted((rng * (rng - 1) / 2), N)]
	return False if comb(n, 2) != N else x.ndim == 1 and n == int(n)

def is_point_cloud(x: ArrayLike) -> bool: 
	"""Checks whether 'x' is a 2-d array of points"""
	return(isinstance(x, np.ndarray) and x.ndim == 2)

def is_dist_like(x: ArrayLike):
	"""Checks whether _x_ is any recognizable distance object."""
	return(is_distance_matrix(x) or is_pairwise_distances(x))

def as_pairwise_dist(x: ArrayLike) -> ArrayLike:
	"""Converts an arbitrary input to a set of pairwise distances"""
	from scipy.spatial.distance import pdist 
	if is_point_cloud(x):
		pd = pdist(x)
	elif is_dist_like(x):
		pd = np.tril(x) if is_distance_matrix(x) else x
	else: 
		raise ValueError("Unknown input shape 'x' ")
	return pd