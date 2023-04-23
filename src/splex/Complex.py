
from __future__ import annotations # for mypy to recognize self return types
from numbers import Number, Integral
from dataclasses import dataclass
from more_itertools import collapse, unique_justseen
from .meta import *   
from .generics import *

# class ComplexBase(ComplexLike):
#   """Base class for comparable complex-like classes with integer vertex labels."""
#   def __repr__(self) -> str:
#     if len(self) == 0:
#       return "< Empty simplicial complex >"
#     return f"{type(self).__name__} with {card(self)} {tuple(range(0,dim(self)+1))}-simplices"

