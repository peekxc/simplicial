
import griffe.dataclasses as dc
import griffe.docstrings.dataclasses as ds

from quartodoc import get_object
from quartodoc.renderers import MdRenderer
from plum import dispatch
from typing import *

class NumpyRenderer(MdRenderer):
  def __init__(self, header_level: int = 1):
    self.header_level = header_level

  @dispatch
  def render(self, el):
    import warnings 
    warnings.warn(f"Unsupport type {type(el)}")
    # raise NotImplementedError(f"Unsupported type: {type(el)}")
  
  @dispatch
  def render(self, el: ds.DocstringSectionParameters) -> str:
    params_str = []
    for ds_param in el.value:
      d = ds_param.as_dict()
      pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
      sec_md = f"**{pn}** : "
      if isinstance(pa, Name) or isinstance(pa, Expression):
        sec_md += f"<span class='type_annotation'> {pa.full}, </span>"
      else: 
        sec_md += "" if pa is None or len(str(pa)) == 0 else str(pa)+", "
      sec_md += f"optional (default={ d.get('value') })" if "value" in d.keys() else "required"
      sec_md += f"<p> {pd} </p>" #style='margin-top: 10px;margin-left: 2.5em;
      params_str.append(sec_md)
    return "\n\n".join(params_str)

  @dispatch
  def render(self, el: dc.Docstring):
    return f"A docstring with {len(el.parsed)} pieces"


