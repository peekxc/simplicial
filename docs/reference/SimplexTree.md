# SimplexTree

 --- 

SimplexTree provides lightweight wrapper around a Simplex Tree data structure: an ordered, trie-like structure whose nodes are in bijection with the faces of the complex. 
This class exposes a native extension module wrapping a simplex tree implemented with modern C++.

 --- 

## insert { #insert }

`insert(self, simplices: Iterable[SimplexLike])`

Inserts simplices into the Simplex Tree. 

Note inserting a simplex by definition also inserts all of its faces. If the simplex exists, the tree is not modified. 

### Parameters

| Name        | Type                  | Description                                                     | Default   |
|-------------|-----------------------|-----------------------------------------------------------------|-----------|
| `simplices` | Iterable[SimplexLike] | Iterable of simplices to insert (each of which are SimplexLike) | required  |

Note: 
  If the iterable is an 2-dim np.ndarray, then a p-simplex is inserted along each contiguous p+1 stride.
  Otherwise, each element of the iterable to casted to a Simplex and then inserted into the tree.

 --- 

## remove { #remove }

`remove(self, simplices: Iterable)`

 --- 

## find { #find }

`find(self, simplices: Iterable)`

 --- 

## adjacent { #adjacent }

`adjacent(self, simplices: Iterable)`

 --- 

## collapse { #collapse }

`collapse(self, sigma: SimplexLike, tau: SimplexLike)`

 --- 

## degree { #degree }

`degree(self, vertices: Optional[ArrayLike] = None)`

Computes the degree of select vertices in the trie.

### Parameters

| Name       | Type                   | Description                                                                                                                      | Default   |
|------------|------------------------|----------------------------------------------------------------------------------------------------------------------------------|-----------|
| `vertices` | numpy.typing.ArrayLike | Retrieves vertex degrees If no vertices are specified, all degrees are computed. Non-existing vertices by default have degree 0. | `None`    |

Returns: 
  list: degree of each vertex id given in 'vertices'

 --- 

## traverse { #traverse }

`traverse(order: str = 'preorder', f: Callable = print, kargs)`

### Parameters

| Name       | Type   | Description                                                                  | Default      |
|------------|--------|------------------------------------------------------------------------------|--------------|
| `order`    |        | the type of traversal to do                                                  | `'preorder'` |
| `f`        |        | a function to evaluate on every simplex in the traversal. Defaults to print. | `print`      |
| `**kwargs` |        | additional arguments to the specific traversal.                              | required     |

 --- 

## cofaces { #cofaces }

`cofaces(self, p: int = None, sigma: SimplexLike = [])`

### Parameters

| Name    | Type   | Description                      | Default   |
|---------|--------|----------------------------------|-----------|
| `p`     |        | coface dimension to restrict to  | `None`    |
| `sigma` |        | the simplex to obtain cofaces of | `[]`      |

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

Performs a k-expansion of the tree.

Parameters: 
  k : maximum dimension to expand to.