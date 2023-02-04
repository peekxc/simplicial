from quartodoc import MdRenderer
from griffe import dataclasses as dc
from griffe.docstrings import dataclasses as ds
from plum import dispatch
from tabulate import tabulate
from typing import *
from griffe.expressions import Name, Expression
from quartodoc.renderers import *

_UNHANDLED = []

## NOTE: CAREFUL! DISPATCH DEFINITION ORDER MATTERS HERE!
class MdRendererNumpyStyle(MdRenderer):
  style = "markdown_numpy"

  def __init__(
    self,
    header_level: int = 2,
    show_signature: bool = True,
    show_signature_annotations: bool = False,
    display_name: str = "name",
    hook_pre=None,
  ):
    self.header_level = header_level
    self.show_signature = show_signature
    self.show_signature_annotations = show_signature_annotations
    self.display_name = display_name
    self.hook_pre = hook_pre
  
  def _render_annotation(self, el: "str | dc.Name | dc.Expression | None"):
    if isinstance(el, (type(None), str)):
      return el
    return el.full.replace("|", "\\|")

  def _fetch_object_dispname(self, el: "dc.Alias | dc.Object"):
    if self.display_name == "name":
      return el.name
    elif self.display_name == "relative":
      return ".".join(el.path.split(".")[1:])
    elif self.display_name == "full":
      return el.path
    elif self.display_name == "canonical":
      return el.canonical_path
    elif self.display_name == "parent":
      return el.parent.name + "." + el.name
    raise ValueError(f"Unsupported display_name: `{self.display_name}`")
  
  # Keep admonition at the top here ----
  @dispatch
  def render(self, el: ds.DocstringSectionAdmonition) -> str:
    _UNHANDLED.append(el)
    return "UNHANDLED ADMONITION"


  ## Most general 
  @dispatch
  def render(self, el: Union[dc.Object, dc.Alias]):
    # return super(MdRendererNumpyStyle, self).render(el)
    _str_dispname = self._fetch_object_dispname(el)
    _str_pars = self.render(el.parameters)
    str_sig = f"`{_str_dispname}({_str_pars})`"

    _anchor = f"{{ #{_str_dispname} }}"
    str_title = f"{'#' * self.header_level} {_str_dispname} {_anchor}"

    str_body = []
    if el.docstring is None:
      pass
    else:
      for section in el.docstring.parsed:
        new_el = docstring_section_narrow(section)
        title = new_el.title if new_el.title is not None else new_el.kind.value
        body = self.render(new_el)
        if title != "text":
          header = f"{'#' * (self.header_level + 1)} {title.title()}"
          str_body.append("\n\n".join([header, body]))
        else:
          str_body.append(body)

    parts = [str_title, str_sig, *str_body] if self.show_signature else [str_title, *str_body]
    return "\n\n".join(parts)

  # Parameters ----
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
      sec_md += f"<p> {pd} </p>" 
      params_str.append(sec_md)
    return "\n\n".join(params_str)

  @dispatch
  def render(self, el: dc.Parameters):
    return ", ".join(map(self.render, el))
    # return super(MdRendererNumpyStyle, self).render(el)

  @dispatch
  def render(self, el: dc.Parameter):
    splats = {dc.ParameterKind.var_keyword, dc.ParameterKind.var_positional}
    has_default = el.default and el.kind not in splats
    annotation = self._render_annotation(el.annotation)
    if self.show_signature_annotations:
      if annotation and has_default:
        return f"{el.name}: {el.annotation} = {el.default}"
      elif annotation:
        return f"{el.name}: {el.annotation}"
    elif has_default:
      return f"{el.name}={el.default}"
    return el.name
    #  return super(MdRendererNumpyStyle, self).render(el)

  # returns ----
  @dispatch
  def render(self, el: Union[ds.DocstringSectionReturns, ds.DocstringSectionRaises]) -> str:
    params_str = []
    for ds_param in el.value:
      d = ds_param.as_dict()
      pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
      sec_md = f"**{pn}** : "
      if isinstance(pa, Name) or isinstance(pa, Expression):
        sec_md += f"<span class='type_annotation'> {pa.full}, </span>"
      else: 
        sec_md += "" if pa is None or len(str(pa)) == 0 else str(pa)+", "
      sec_md += f"<p> {pd} </p>" #style='margin-top: 10px;margin-left: 2.5em;
      params_str.append(sec_md)
    return "\n\n".join(params_str)

  @dispatch
  def render(self, el: Union[ds.DocstringReturn, ds.DocstringRaise]):
    # similar to DocstringParameter, but no name or default
    # annotation = self._render_annotation(el.annotation)
    # return (annotation, el.description)
    return "RETURNS"

  # --- Attributes
  @dispatch
  def render(self, el: ds.DocstringAttribute) -> str :
    _UNHANDLED.append(el)
    d = ds_attr.as_dict()
    pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
    # return [pn, self._render_annotation(pa), pd]
    return "UNHANDLED ATTRIBUTE" 

  @dispatch
  def render(self, el: ds.DocstringSectionAttributes):
    header = ["Name", "Type", "Description"]
    # _UNHANDLED.append(el)
    # rows = list(map(self.render, el.value))
    rows = []
    for ds_attr in el.value:
      d = ds_attr.as_dict()
      pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
      rows.append([pn, self._render_annotation(pa), pd])
    return tabulate(rows, header, tablefmt="github")

  ## examples ----
  @dispatch
  def render(self, el: ds.DocstringSectionExamples) -> str:
    return super(MdRendererNumpyStyle, self).render(el)
  
  @dispatch
  def render(self, el: ExampleCode) -> str:
    return super(MdRendererNumpyStyle, self).render(el)

  ## Sections ---   
  @dispatch
  def render(self, el: ds.DocstringSectionText):
    new_el = docstring_section_narrow(el)
    if isinstance(new_el, ds.DocstringSectionText):
      return el.value # ensures we don't recurse forever
    return self.render(new_el)  

  @dispatch
  def render(self, el: ds.DocstringSection):
    _UNHANDLED.append(el)
    return "UNHANDLED SECTION"

  @dispatch
  def render(self, el: ExampleText):
    return "```{python}\n" + el.value + "\n```"

  @dispatch
  def render(self, el) -> str:
    #raise NotImplementedError(f"Unsupported type of: {type(el)}")
    _UNHANDLED.append(el)
    import warnings
    warnings.warn(f"Unsupported type of: {type(el)}")
    return ""


