[![Tests](https://github.com/peekxc/splex/actions/workflows/package.yml/badge.svg)](https://github.com/peekxc/splex/actions/workflows/package.yml)
[![coverage_badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/peekxc/ef42349965f40edf4232737026690c5f/raw/coverage_info.json)](https://coveralls.io/github/peekxc/splex)
[![python_badge](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://github.com/peekxc/splex/actions/workflows/python-package.yml)
[![coverage_badge](https://img.shields.io/github/actions/workflow/status/peekxc/splex/build-macos.yml?logo=apple&logoColor=white)](https://github.com/peekxc/splex/actions/workflows/build-macos.yml)
[![coverage_badge](https://img.shields.io/github/actions/workflow/status/peekxc/splex/build-windows.yml?logo=windows&logoColor=white)](https://github.com/peekxc/splex/actions/workflows/build-windows.yml)
[![coverage_badge](https://img.shields.io/github/actions/workflow/status/peekxc/splex/build-linux.yml?logo=linux&logoColor=white)](https://github.com/peekxc/splex/actions/workflows/build-linux.yml)

`splex` is a Python package aimed at providing common, _pythonic_ interface for constructing and manipulating [abstract simplicial complexes](https://en.wikipedia.org/wiki/Abstract_simplicial_complex) that is efficient and representation independent. Part of the package API was inspired by how [NetworkX](https://networkx.org/documentation/stable/index.html) handles graph data. 

Longer term, the goal of `splex` is to provide simple and performant implementations of common scientific operations on complexes in ways that are highly interoperable with the rest of the scientific Python ecosystem (e.g. SciPy, NumPy). For example, one objective to provide efficient ways to construct boundary (+Laplacian) [sparse matrices](https://docs.scipy.org/doc/scipy/reference/sparse.html) and [operators](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html) from _any_ simplicial complex. Other operations, such as e.g. random complex generation, geometric realizations, and sparsification algorithms are also planned. 

> __NOTE__: `splex` is early-stage software primarily used for research currently, and many common simplicial operations are not yet provided (e.g. simplicial maps, sparsification)---if you’re interested in using `splex` but need some specific functionality, please open an issue.

## Installation 

```
python -m pip install -e git+https://github.com/peekxc/splex.git#egg=splex
```

## Documentation 

Documentation available [here](https://peekxc.github.io/splex/)

## Quickstart 

```python
s = Simplex([0,1,2])                       # Explicit simplex class for value and set-like semantics
S = simplicial_complex([[0,1,2], [4,5]])   # Complexes are constructible from myriad of types
K = filtration(S, weight=lambda s: max(s)) # Filtrations are easy to specify via functions 


## All the types are pythonic and easy to use  
K.print()
K.add(...)
K.remove(...)
K.update(...)

## But also come with specific functionality 
K.reindex(...)

## Complexes are representation-independent..
S = simplicial_complex(S, form='tree') # convert to tree-based
S = simplicial_complex(S, form='rank') # convert to array-based

## as are generic functions
from splex.generics import faces, card, dim
for s in faces(S):
  ...
```

For more details, see the documentation. 

## Motivation 

What if there was a natural type for representing simplices? 
```python
s, t = Simplex([0,1,2]),  Simplex([0,1])

print(s.dim(), ":", s)
# 2 : (0,1,2)

t < s, t <= s, s < t
# True, True, False

t in s.boundary()
# True 

print(list(s.faces()))
# [(0), (1), (2), (0,1), (0,2), (1,2), (0,1,2)]
```

What if said type was flexible and easy to work with, supporting no-fuss construction

```python
Simplex(2) == Simplex([2])                      # value-types are always unboxed 
Simplex([1,2]) == Simplex([1, 2, 2])            # simplices have unique entries, are hashable 
Simplex((1,5,3)) == Simplex(np.array([5,3,1]))  # arrays and tuples supported out of the box 
Simplex((0,1,2)) == Simplex(range(3))           # ... as are generators, iterables, collections, etc
```

What if it was easy to use with other native Python tools?
```python
s = Simplex([0,1,3,4])
np.array(s)          # native __array__ conversion enabled
len(s)               # __len__ is as expected 
3 in s               # __contains__ acts vertex-wise
list(iter(s))        # __iter__ also acts vertex-wise
s[0]                 # __getitem__ as well 
s[0] = 5             # __setitem__ is *not*: Simplices are immutable!

# Which means native support for the expected protocols 
isinstance(s, Sized)     # True 
isinstance(s, Container) # True 
isinstance(s, Iterable)  # True 
isinstance(s, Mapping)   # False 
```

What if there was a similar construction for simplicial complexes?
```python
S = simplicial_complex([[0,1,2,3], [4,5], [6]])
print(S)
# 3-d complex with (7, 7, 4, 1)-simplices of dimension (0, 1, 2, 3)

[s for s in S.faces()] # [(0), (1), ..., (1,2,3), (0,1,2,3)]
S.add([5,6]) # adds Simplex([5,6]) to the complex 
```

.. and for filtered complexes as well?
```python
K = filtration(enumerate(S)) # index-ordered filtration
print(K)
# 3-d filtered complex with (7, 7, 4, 1)-simplices of dimension (0, 1, 2, 3)
print(format(K))
# 3-d filtered complex with (7, 7, 4, 1)-simplices of dimension (0, 1, 2, 3)
# I: 0   ≤ 1   ≤ 2   ≤ 3   ≤ 4   ≤  ...  ≤ 17      ≤ 18       
# S: (0) ⊆ (1) ⊆ (2) ⊆ (3) ⊆ (4) ⊆  ...  ⊆ (1,2,3) ⊆ (0,1,2,3)

[s for s in K.faces()] # [(0), (1), ..., (1,2,3), (0,1,2,3)]
```

What if there were multiple choices in representation...


```python
SS = simplicial_complex([[0,1,2,3]], form="set")  # simplices stored as collections in a set 
ST = simplicial_complex([[0,1,2,3]], form="tree") # simplices stored as nodes in a tree 
SR = simplicial_complex([[0,1,2,3]], form="rank") # simplices stored as integers in an array 
# ... 
```

...but every representation was supported through _generics_


```python
faces(SS)           # calls overloaded .faces()
faces(ST)           # same as above, but using a simplex tree
faces(SR)           # same as above, but using a rank complex 
faces([[0,1,2,3]])  # same as above! Falls back to combinations! 
# same goes for .card(), .dim(), .boundary(), ...
```

What if extending support to all such types generically was as easy as

```python
def faces(S: ComplexLike) -> Iterator[SimplexConvertible]:
  if hasattr(S, "faces"):
    yield from S.faces()
  else:
    ...
```

...where `ComplexLike` is a [protocol](https://mypy.readthedocs.io/en/stable/protocols.html) defining a minimal interface needed for Python types to be interpreted as complexes. This is duck typing---no nominal inheritance needed! Just define your type, make it _pythonic_ via abc.collections and go. 


```python
from typing import *
from splex.meta import SimplexConvertible, ComplexLike 

class MyCellComplex:
  def __iter__(self) -> Iterator[SimplexConvertible]:
    ... # < specific implementation > 
```



