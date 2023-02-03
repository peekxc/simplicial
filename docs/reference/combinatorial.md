## rank_C2 { #rank_C2 }

`rank_C2(i: int, j: int, n: int)`

 --- 

## unrank_C2 { #unrank_C2 }

`unrank_C2(x: int, n: int)`

 --- 

## unrank_lex { #unrank_lex }

`unrank_lex(r: int, k: int, n: int)`

 --- 

## rank_lex { #rank_lex }

`rank_lex(c: Iterable, n: int)`

 --- 

## rank_colex { #rank_colex }

`rank_colex(c: Iterable)`

 --- 

## unrank_colex { #unrank_colex }

`unrank_colex(r: int, k: int)`

Unranks a k-combinations rank 'r' back into the original combination in colex order

From: Unranking Small Combinations of a Large Set in Co-Lexicographic Order

 --- 

## rank_combs { #rank_combs }

`rank_combs(C: Iterable[tuple], n: int = None, order: str = ['colex', 'lex'])`

Ranks k-combinations to integer ranks in either lexicographic or colexicographical order

Parameters: 
  C : Iterable of combinations 
  n : cardinality of the set (lex order only)
  order : the bijection to use

Returns: 
  list : unsigned integers ranks in the chosen order.

 --- 

## unrank_combs { #unrank_combs }

`unrank_combs(R: Iterable[int], k: Union[int, Iterable], n: int = None, order: str = ['colex', 'lex'])`

Unranks integer ranks to  k-combinations in either lexicographic or colexicographical order

Parameters: 
  R : Iterable of integer ranks 
  n : cardinality of the set (lex order only)
  order : the bijection to use

Returns: 
  list : k-combinations derived from R