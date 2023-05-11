from .SetFiltration import * 
from .RankFiltration import * 
from functools import partial

def filtration(simplices: Iterable[SimplexConvertible], f: Optional[Callable] = None, form: Optional[str] = "default", **kwargs):
  form = "set" if form is None or form == "default" else form
  if f is None: 
    index_map = { s:i for i, s in enumerate(simplices) }
    f = partial(lambda s, d: d[s], d=index_map)
  if form == "set":
    sf = SetFiltration(simplices, f, **kwargs)
  elif form == "rank":
    sf = RankFiltration(simplices, f, **kwargs)
  else: 
    raise ValueError(f"Unknown data structure '{str(type(form))}'.")
  return sf