[![Python package](https://github.com/peekxc/splex/actions/workflows/python-package.yml/badge.svg)](https://github.com/peekxc/splex/actions/workflows/python-package.yml)


<!-- [![Appveyor Windows Build status](https://img.shields.io/appveyor/ci/peekxc/splex/master.svg?logo=windows&logoColor=DDDDDD)](https://github.com/peekxc/splex/actions/workflows/python-package.yml)
[![Travis OS X Build status](https://img.shields.io/travis/peekxc/splex/master.svg?logo=Apple&logoColor=DDDDDD&env=BADGE=osx&label=build)](https://github.com/peekxc/splex/actions/workflows/python-package.yml)
[![Travis Linux X Build status](https://github.com/peekxc/splex/actions/workflows/python-package.yml)](https://travis-ci.com/peekxc/splex) --> 
<!-- [![Coverage Status](https://coveralls.io/repos/github/peekxc/splex/badge.svg?branch=main)](https://coveralls.io/github/peekxc/splex?branch=main) -->

`splex` is an experimental package for constructing, manipulating, and computing with simplicial complexes. 

## Quickstart 

What if there was a natural type for representing simplices? 
```{python}
from splex import Simplex
s, t = Simplex([0,1,2]),  Simplex([0,1])

print(s.dim(), ":", s)
# 2 : (0,1,2)

## Supports face relations
t < s 
# True 

## Has a boundary
t in s.boundary()
# True 

## Can enumerate its faces
print(list(s.faces()))
# [(0), (1), (2), (0,1), (0,2), (1,2), (0,1,2)]
```

What if said type was easy to work with, having no-fuss construction?

```{python}
Simplex(2) == Simplex([2])                        # value-types are always unboxed 
Simplex([1,2]) == Simplex([1, 2, 2])              # simplices have set-like semantics, are hashable 
Simplex((1,5,3)) == Simplex(np.array([5,3,1]))    # arrays, tuples, collections supported out of the box 
Simplex((0,1,2)) == Simplex(range(3))             # ... as are generators and iterables 
```

What if it was easy to use with other native Python tools?
```{python}
s = Simplex([0,1,3,4])
np.array(s)          # native __array__ conversion enabled
len(s)               # __len__ is as expected 
3 in 3               # __contains__ acts vertex-wise
list(iter(s))        # __iter__ also acts vertex-wise
s[0]                 # __getitem__ as well 
s[0] = 5             # __setitem__ is *not*: Simplices are immutable!

# Which means native support for the expected protocols 
isinstance(s, Sized)     # True 
isinstance(s, Container) # True 
isinstance(s, Iterable)  # True 
isinstance(s, Mapping)   # False 

# combinations yield Simplex types
all([t <= s for t in combinations(s, 2)]) # True 
```

What if there was a similar construction for simplicial complexes?
```{python}
S = simplicial_complex([[0,1,2,3], [4,5], [6]])
print(S)
# 3-d complex with (7, 7, 4, 1)-simplices of dimension (0, 1, 2, 3)

[s for s in S.faces()] # [(0), (1), ..., (1,2,3), (0,1,2,3)]
S.add([5,6]) # adds Simplex([5,6]) to the complex 
```

.. and for filtered complexes as well?
```{python}
K = filtration()
print(K)


```

What if there were multiple choices in representation...


```{python}

```

...but every representation was supported through generics


```{python}

```

What if extending support to all such types was as easy as

```{python}

```

...where `ComplexLike` is a protocol class defining a minimal interface, i.e. 

```{python}

```

No direct inheritance needed. Just define your type, make it _pythonic_, and go. Just like Iterable! 


```{python}

```

But what if the types could be *narrowed* for highly performant, type-specific algorithms?

```{python}

```

These are the goals of the `splex` package. Clean, extensible, performant.  

