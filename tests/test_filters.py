import numpy as np
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
