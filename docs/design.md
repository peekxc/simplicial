# Simplicial Design Philosophy

Suppose you wanted to represent a [combinatorial n-simplex](https://en.wikipedia.org/wiki/Abstract_simplicial_complex). Why not use a built-in [sequence](https://docs.python.org/3/glossary.html#term-sequence) type?

```python
simplex = [0,1,2] # why note use a list? 
```

But wait, simplices are simple value objects, just like strings (`'abc'`) or integers (`123`), which are [immutable](https://docs.python.org/3/faq/design.html#why-are-python-strings-immutable) and [hashable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Hashable). Perhaps a `tuple` then? 

```python
simplex = (0,1,2)
```

But wait, simplices are _set-like_: they have unique entries and are [comparable](https://portingguide.readthedocs.io/en/latest/comparisons.html). But `(0,1,1,1,1,2)` is clearly not a simplex, though it is immutable. How about a set?

```
simplex = set([0,1,2])
```

Sets actually are naturally comparable and have unique entries: 

```python
face = set([1,2])
face <= simplex # True
set([2,1,0,1]) == simplex # True 
```

But ahhh, they are also mutable! How about frozenset? 

```python
simplex = frozenset([0,1,2])
```

Immutable, comparable, unique... this seems fine. Except it's elements are not _homogenous_ 

```
simplex = frozenset([0,1,'a',2,'b'])
```

There's no *technical* reason not use non-type-homogenous vertex sets---however, mixing types may imply different per-element memory layouts, and comparability between elements becomes muddled. 

Indeed, it seems the Python data model [doesn't have an immutable, homogenous, set-like container](https://stackoverflow.com/questions/66874287/python-data-model-type-protocols-magic-methods). 

- lists are mutable, non-homogenous, and non-hashable
- tuples are comparable and immutable, but they are not _set like_
- frozensets are comparable, immutable, and set-like, but are neither homogenous nor ordered
- the (non-standard) _SortedSet_ is comparable, set-like, and ordered, but it is neither _immutable_ nor _hashable_.
- array & np.array are homogeous collections, but they are mutable and not _set like_
- bytes are comparable, immutable, and homogenous, lacking only _set like_, functionality---however their values are limited to [0, 255]

One concludes there is no off-the-shelf Python class that is completely appropriate for a simplex. So, let's make our own!

## The Simplex Class

```python
class Simplex(Hashable):
  pass
```


### Usage 


As an aside, Python affectuionados may point to the fact that most of the above process of designing a class can be heavily side-stepped using various decorators patterns, like Python's [dataclasses](https://docs.python.org/3/library/dataclasses.html). For example, here's a very similar class to the one above. 

```python
@dataclass(frozen=True)
class Simplex(Collection[int]):
  vertices = field(default_factory=SortedSet, compare=True) 
```

## The elephant in the room: Performance

Let's see how performant our simplex type is. 

```{code-block}

```

Now suppose, we replace this with a simple numpy-based solution. 

```{code-block}

```

After all this effort, the class definition of a simplex seems _nuaced_ & _complex_ from an optimistic perspective---though from a pessimistic one it is _pedantic_ & _monolithic_. Although the notions of _comparability_ and its methods seem elegant and natural to use, they hinder the practicality of class. Indeed,  if we're going to be operating on many simplices at a time, it's _far more efficient_ to simply stream operations with a \[numpy\] array!

Of course, none of the type-checking was done with the numpy solution: the computationally tedious parts are hidden in the precondition. This reflects a a general pattern in software-engineering. Check up-front first. 


## Structural Subtyping & Generics

