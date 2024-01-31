import numpy as np
import splex as sx
from splex.filters import *

def test_lower_star():
	assert True

def test_generic_filter():
	from splex.filters import generic_filter
	assert True

def test_fixed_filter():
	from splex.generics import faces
	from splex.filters import fixed_filter
	from splex.complexes import simplicial_complex
	S = simplicial_complex([[0, 1, 2, 3, 4]])
	f = fixed_filter(S, range(len(S)))
	assert np.all(f(S) == np.arange(len(S)))
	assert isinstance(f(faces(S, 1)), np.ndarray)
	assert f(Simplex([0, 1, 2])) == 15
	assert f([0, 1, 2]) == 15
	assert isinstance(f(np.array(list(faces(S, 1)))), np.ndarray)

def test_hirola():
	import splex as sx
	for form in ['set', 'rank', 'tree']:
		S = sx.simplicial_complex([[0, 1, 2, 3, 4]], form=form)
		filter_f = sx.filters.HirolaFilter(S, np.arange(len(S)))
		ind = np.take([i for i, s in enumerate(S) if sx.Simplex(s) == (0,1,2)], 0)
		v_ind = np.array([i for i, s in enumerate(S) if sx.dim(s) == 0])
		quad_ind = np.array([i for i, s in enumerate(S) if sx.dim(s) == 3])
		assert isinstance(filter_f, Callable)
		assert filter_f([0,1,2]) == ind
		assert np.all(np.array([filter_f(s) for s in S]) == np.arange(len(S)))
		assert filter_f(((0,1,2))) == ind
		assert np.all(filter_f(sx.faces(S,3)) == quad_ind)
		assert np.all(filter_f(S) == np.arange(len(S)))
		assert np.all(filter_f(sx.faces(S,0)) == v_ind)