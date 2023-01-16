# Representing Simplices 

Suppose you were tasked with designing a _class_ to represent a simplex. Simple, right? It ought to be! 

A simplex 

## Simplex type requirements

The Python data model [doesn't allow](https://stackoverflow.com/questions/66874287/python-data-model-type-protocols-magic-methods) for immutable, hashable, ordered set-like objects.

A few types come close, but have limitations: 
- array & np.array are homogeous collections, but they are mutable are not _unique_ or _set like_
- bytes are comparable, immutable, and homogeous, but their values are limited to [0, 255] and they too are not _set like_
- tuples are comparable and immutable, but they are not _unique_ or _set like_
- frozensets are comparable, immutable, have unique entries, and are set-like, but are *unordered*. 
- the (non-standard) _SortedSet_ is close! However it is _mutable_ and thus not _hashable_.

One concludes there is no core Python representation implementation that is appropriate for a simplex. 
So let's make our own Simplex representation!

## The Design (?)





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

After all this effort, our definition of a simplex seems at best _complex_ and at worst _pedantic_. Although the notions of _comparability_ and its methods seem elegant and natural to use, they hinder the practicality of class. Indeed,  if we're going to be operating on many simplices at a time, it's _far more efficient_ to simply stream operations with a \[numpy\] array!

Of course, none of the type-checking was done with the numpy solution: the computationally tedious parts are hidden in the precondition. This reflects a a general pattern in software-engineering. Check up-front first. 


## Solution: Generics and Structural Subtyping

