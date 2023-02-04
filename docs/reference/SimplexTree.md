# SimplexTree

 --- 

SimplexTree provides lightweight wrapper around a Simplex Tree data structure: an ordered, trie-like structure whose nodes are in bijection with the faces of the complex. 
This class exposes a native extension module wrapping a simplex tree implemented with modern C++.

| Name        | Type    | Description                          |
|-------------|---------|--------------------------------------|
| n_simplices | ndarray | number of simplices                  |
| dimension   | int     | maximal dimension of the complex     |
| id_policy   | str     | policy for generating new vertex ids |

 --- 

## insert { #insert }

`insert(self, simplices: Iterable[SimplexLike])`

Inserts simplices into the Simplex Tree. 

By definition, inserting a simplex also inserts all of its faces. If the simplex already exists in the complex, the tree is not modified. 

### Parameters

**simplices** : <span class='type_annotation'> Iterable[SimplexLike], </span>required<p> Iterable of simplices to insert (each of which are SimplexLike) </p>

Note: 
  If the iterable is an 2-dim np.ndarray, then a p-simplex is inserted along each contiguous p+1 stride.
  Otherwise, each element of the iterable to casted to a Simplex and then inserted into the tree.

 --- 

## remove { #remove }

`remove(self, simplices: Iterable[SimplexLike])`

Removes simplices into the Simplex Tree. 

By definition, removing a face also removes all of its cofaces. If the simplex does not exist in the complex, the tree is not modified. 

### Parameters

**simplices** : <span class='type_annotation'> Iterable[SimplexLike], </span>required<p> Iterable of simplices to insert (each of which are SimplexLike) </p>

Note: 
  If the iterable is an 2-dim np.ndarray, then a p-simplex is inserted along each contiguous p+1 stride.
  Otherwise, each element of the iterable to casted to a Simplex and then inserted into the tree.

 --- 

## find { #find }

`find(self, simplices: Iterable[SimplexLike])`

Finds whether simplices exist in Simplex Tree. 

### Parameters

**simplices** : <span class='type_annotation'> Iterable[SimplexLike], </span>required<p> Iterable of simplices to insert (each of which are SimplexLike) </p>

Note: 
  If the iterable is an 2-dim np.ndarray, then a p-simplex is inserted along each contiguous p+1 stride.
  Otherwise, each element of the iterable to casted to a Simplex and then inserted into the tree. 

Return: 
  ndarray : boolean array for each simplex indicating whether it was found in the complex

 --- 

## adjacent { #adjacent }

`adjacent(self, simplices: Iterable)`

 --- 

## collapse { #collapse }

`collapse(self, tau: SimplexLike, sigma: SimplexLike)`

Checks whether its possible to collapse $\sigma$ through $  au$, and if so, both simplices are removed.

A simplex $\sigma$ is said to be collapsible through one of its faces $     au$ if $\sigma$ is the only coface of $ au$ (excluding $        au$ itself). 

Parameters: 
  sigma : maximal simplex to collapse
  tau : face of sigma to collapse 

### Returns

**bool** : None, <p> whether the pair was collapsed </p>

Example: 
  >>> st = SimplexTree([[0,1,2]])
  >>> print(st)
  Simplex Tree with (3, 3, 1) (0, 1, 2)-simplices

  >>> st.collapse([1,2], [0,1,2])
  True 

  >>> print(st)
  Simplex Tree with (3, 2) (0, 1)-simplices

 --- 

## vertex_collapse { #vertex_collapse }

`vertex_collapse(self, u: int, v: int, w: int)`

Maps a pair of vertices into a single vertex. 

### Parameters

**u** : <span class='type_annotation'> int, </span>required<p> the first vertex in the free pair. </p>

**v** : <span class='type_annotation'> int, </span>required<p> the second vertex in the free pair.  </p>

**w** : <span class='type_annotation'> int, </span>required<p> the target vertex to collapse to. </p>

 --- 

## degree { #degree }

`degree(self, vertices: Optional[ArrayLike] = None)`

Computes the degree of select vertices in the trie.

### Parameters

**vertices** : <span class='type_annotation'> numpy.typing.ArrayLike, </span>optional (default=None)<p> Retrieves vertex degrees
If no vertices are specified, all degrees are computed. Non-existing vertices by default have degree 0.  </p>

Returns: 
  list: degree of each vertex id given in 'vertices'

 --- 

## traverse { #traverse }

`traverse(order: str = 'preorder', f: Callable = print, sigma: SimplexLike = [], p: int = 0)`

Traverses the simplex tree in the specified order, calling 'f' on each simplex encountered

Supported traversals: 
  - breadth-first ("bfs") 

### Parameters

**order** : optional (default='preorder')<p> the type of traversal to do  </p>

**f** : optional (default=print)<p> a function to evaluate on every simplex in the traversal. Defaults to print.  </p>

**sigma** : optional (default=[])<p> simplex to start the traversal at, where applicable. Defaults to the root node (empty set) </p>

**p** : optional (default=0)<p> dimension of simplices to restrict to, where applicable. </p>

 --- 

## cofaces { #cofaces }

`cofaces(self, p: int = None, sigma: SimplexLike = [])`

### Parameters

**p** : optional (default=None)<p> coface dimension to restrict to  </p>

**sigma** : optional (default=[])<p> the simplex to obtain cofaces of </p>

Returns: 
  list: the p-cofaces of sigma

 --- 

## coface_roots { #coface_roots }

`coface_roots(self, p: int = None, sigma: SimplexLike = [])`

 --- 

## skeleton { #skeleton }

`skeleton(self, p: int = None)`

 --- 

## simplices { #simplices }

`simplices(self, p: int = None, sigma: SimplexLike = [])`

 --- 

## maximal { #maximal }

`maximal(self)`

 --- 

## link { #link }

`link(self, sigma: SimplexLike = [])`

 --- 

## expand { #expand }

`expand(self, k: int)`

Performs a k-expansion of the complex.

This function is particularly useful for expanding clique complexes beyond their 1-skeleton. 

Parameters: 
  k : maximum dimension to expand to. 

### Examples

```python
>>> st = SimplexTree(combinations(range(8), 2))
>>> print(st)
    Simplex Tree with (8, 28) (0, 1)-simplices
>>> st.expand(k=2)
>>> print(st)
    Simplex Tree with (8, 28, 56) (0, 1, 2)-simplices
```