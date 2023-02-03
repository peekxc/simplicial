import numpy as np 
from typing import * 
from itertools import * 
from numbers import Integral
from math import comb, factorial
# import _combinatorial as comb_mod

def rank_C2(i: int, j: int, n: int) -> int:
  i, j = (j, i) if j < i else (i, j)
  return(int(n*i - i*(i+1)/2 + j - i - 1))

def unrank_C2(x: int, n: int) -> tuple:
  i = int(n - 2 - np.floor(np.sqrt(-8*x + 4*n*(n-1)-7)/2.0 - 0.5))
  j = int(x + i + 1 - n*(n-1)/2 + (n-i)*((n-i)-1)/2)
  return(i,j) 

def unrank_lex(r: int, k: int, n: int):
  result = np.zeros(k, dtype=np.uint16)
  x = 1
  for i in range(1, k+1):
    while(r >= comb(n-x, k-i)):
      r -= comb(n-x, k-i)
      x += 1
    result[i-1] = (x - 1)
    x += 1
  return(result)

def rank_lex(c: Iterable, n: int) -> np.uint64:
  c = np.sort(np.fromiter(c, dtype=np.uint16))
  index = sum([comb(cc, kk) for cc,kk in zip((n-1)-c, np.flip(range(1, len(c)+1)))])
  return np.uint64((comb(n, len(c))-1) - int(index))

def rank_colex(c: Iterable) -> int:
  c = np.sort(np.fromiter(c, dtype=np.uint16))
  return sum([comb(ci, i+1) for i,ci in zip(reversed(range(len(c))), reversed(c))])


def unrank_colex(r: int, k: int) -> np.ndarray:
  """
  Unranks a k-combinations rank 'r' back into the original combination in colex order
  
  From: Unranking Small Combinations of a Large Set in Co-Lexicographic Order
  """
  c = np.zeros(k, dtype=np.uint16)
  for i in reversed(range(1, k+1)):
    m = i
    while r >= comb(m,i):
      m += 1
    c[i-1] = m-1
    r -= comb(m-1,i)
  return c

def rank_combs(C: Iterable[tuple], n: int = None, order: str = ["colex", "lex"]):
  """
  Ranks k-combinations to integer ranks in either lexicographic or colexicographical order
  
  Parameters: 
    C : Iterable of combinations 
    n : cardinality of the set (lex order only)
    order : the bijection to use
  
  Returns: 
    ndarray: unsigned integers ranks in the chosen order.
  """
  if (isinstance(order, list) and order == ["colex", "lex"]) or order == "colex":
    return np.array([rank_colex(c) for c in C], dtype = np.uint64)
  else:
    assert n is not None, "Cardinality of set must be supplied for lexicographical ranking"
    return(np.array([rank_comb(c, len(c), n) for c in C], dtype=np.uint64))

def unrank_combs(R: Iterable[int], k: Union[int, Iterable], n: int = None, order: str = ["colex", "lex"]):
  """
  Unranks integer ranks to  k-combinations in either lexicographic or colexicographical order
  
  Parameters: 
    R : Iterable of integer ranks 
    n : cardinality of the set (lex order only)
    order : the bijection to use
  
  Returns: 
    Union[ndarray, list] : k-combinations, as a list if k is Iterable, otherwise as an array if k is fixed
  """
  if (isinstance(order, list) and order == ["colex", "lex"]) or order == "colex":
    if isinstance(k, Integral):
      return np.array([unrank_colex(r, k) for r in R], dtype = np.int64)
    else: 
      assert len(k) == len(R), "If 'k' is an iterable it must match the size of 'R'"
      return [unrank_colex(r, l) for l, r in zip(k,R)]
  else: 
    assert n is not None, "Cardinality of set must be supplied for lexicographical ranking"
    if isinstance(k, Integral):
      if k == 2: 
        return(np.array([unrank_C2(r, n) for r in R], dtype=np.uint16))
      else: 
        return(np.array([unrank_lex(r, k, n) for r in R], dtype=np.uint16))
    else:
      assert len(k) == len(R), "If 'k' is an iterable it must match the size of 'R'"
      return [unrank_lex(r, l) for l, r in zip(k,R)]