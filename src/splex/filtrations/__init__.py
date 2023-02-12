from .SetFiltration import * 
from .RankFiltration import * 

def filtration(simplices: Iterable[SimplexConvertible], f: Optional[Callable] = None, ds: Optional[str] = "default", **kwargs):
  if ds == "set":
    sc = SetFiltration(simplices, f, **kwargs)
  elif ds == "rank":
    sc = RankFiltration(simplices, f, **kwargs)
  else: 
    raise ValueError(f"Unknown data structure '{str(type(ds))}'.")
  return sc