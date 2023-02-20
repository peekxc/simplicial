# ---
# jupyter: python3
# ---

import os 
from typing import *
from pathlib import Path
from plum import dispatch

from griffe import dataclasses as dc
from griffe.docstrings import dataclasses as ds
from griffe.dataclasses import Docstring
from griffe.loader import GriffeLoader
from griffe.docstrings.parsers import Parser, parse

griffe = GriffeLoader(docstring_parser=Parser("google"))
mod = griffe.load_module("splex")
auto_summaries = {}
ds_elements = {}

## Reload the local file for quick edits
from quartodoc import MdRenderer
from quartodoc.renderers import Renderer
import importlib
import renderers
# importlib.reload(renderers)

## Choose the custom renderer
from renderers import MdRendererNumpyStyle, _UNHANDLED
# if 'markdown_numpy' in Renderer._registry:
#   del Renderer._registry['markdown_numpy']
renderer = MdRendererNumpyStyle(show_signature=True, show_signature_annotations=True, display_name="parent")

class AutoSummary:
  def __init__(self, dir_name: str):
    self.dir_name = dir_name

  @staticmethod
  def full_name(el):
    return f"{el.parent.canonical_path}.{el.name}"

  @staticmethod
  def base_name(el):
    return f"{el.parent.name}.{el.name}"

  @staticmethod
  def parent_name(el):
    return f"{el.parent.name}"

  @dispatch
  def visit(self, el):
    #raise TypeError(f"Unsupported type: {type(el)}")
    import warnings
    warnings.warn(f"Unsupported type: {type(el)}")
    pass

  @dispatch
  def visit(self, el: dc.Module):
    print(f"MOD: {el.canonical_path}")
    for name, class_ in el.classes.items():
      ds_elements.setdefault("MOD", []).append(el)
      self.visit(class_)

    for name, func in el.functions.items():
      self.visit(func)

    for name, mod in el.modules.items():
      self.visit(mod)

  @dispatch
  def visit(self, el: dc.Class):
    if el.name.startswith("_"):
      return
    print(f"CLASS: {self.full_name(el)}")
    ds_elements.setdefault("CLASS", []).append(el)
    auto_summaries.setdefault(el.name, [f"# {el.name}"]).append(renderer.render(el))
    for name, method in el.members.items():
      self.visit(method)

  @dispatch
  def visit(self, el: dc.Alias):
    print(f"ALIAS: {self.full_name(el)}")
    return None

  @dispatch
  def visit(self, el: dc.Function):
    if el.name.startswith("_"):
      return
    print(f"FUNCTION: {self.full_name(el)}, base_name: {self.base_name(el)}")
    ds_elements.setdefault("FUNCTION", []).append(el)
    auto_summaries.setdefault(self.parent_name(el), []).append(renderer.render(el))
    
  @dispatch
  def visit(self, el: dc.Attribute):
    if el.name.startswith("_"):
      return
    print(f"ATTR: {self.full_name(el)}")      
    ds_elements.setdefault("ATTR", []).append(el)


## Create the files
output_dir = os.path.dirname(__file__) + '/reference'
auto = AutoSummary(output_dir)
auto.visit(mod)
p_root = Path(auto.dir_name)
p_root.mkdir(exist_ok=True)
for fn in auto_summaries.keys():
  p_func = p_root / f"{fn}.qmd"
  p_func.write_text("\n\n --- \n\n".join(auto_summaries[fn]))


## TODO: 
## Preprend the following to each doc
## Fix minor formatting issues 
## 
# ---
# format:
#   html:
#     code-fold: false
# jupyter: python3
# execute: 
#   freeze: auto
#   enabled: true
# ---

# ```{python}
# from splex import *
# ```


## Example Parameters 
# el = ds_elements["FUNCTION"][11]
# # p.annotation.full
# print(renderer.render(ds_elements["FUNCTION"][11]))

# from MdRendererExt import GLOBAL_TABS
# header = ["Name", "Type", "Description", "Default"]
# rows, header = GLOBAL_TABS[11]

# from tabulate import tabulate
# print(tabulate(rows, header, tablefmt="github"))

# params = GLOBAL_TABS[11][0]

# for param_name, param_type, param_descr, is_req in params:
#   print(f"{param_name} : _{param_type}_ ({is_req}) \n &nbsp;&nbsp;&nbsp;&nbsp; {param_descr}")
# def filter_invalid_ds(docstrings):
#   if docstrings is None: return []
#   parsed = parse(docstrings, Parser.google)
#   parsed = list(filter(lambda dso: type(dso) != ds.DocstringSectionAdmonition, parsed))
#   return parsed


# splex.SimplexTree.collapse.__doc__
# d = """
# DoFunc.

# Parameters:
#   test: here
#   a : here

# Returns: 
#   b : return description 
# """
# d = """
# Foo.

# d = """
# Example:
#     Examples can be given using either the ``Example`` or ``Examples``
#     sections. Sections support any reStructuredText formatting, including
#     literal blocks::

#         $ python example_google.py
# """
# print(parse(Docstring(d), parser=Parser.google))

# Parameters:
#   reverse: Reverse the generator if `"reverse"` is received.

# Returns:
#   A random integer.
# """
# print(parse(Docstring(d), parser=Parser.google))

# d = """
# Foo.

# Parameters:
#   reverse: Reverse the generator if `"reverse"` is received.

# Returns:
#   A random integer.
# """
# print(parse(Docstring(d), parser=Parser.google))
# parse(Docstring(splex.SimplexTree.collapse.__doc__), parser=Parser.google)

## Choose the extended renderer
# from renderers import MdRendererNumpyStyle
# renderer = MdRendererNumpyStyle(show_signature=True, show_signature_annotations=True, display_name="name")
# renderer._registry[renderer.style] = MdRendererNumpyStyle(show_signature=True, show_signature_annotations=True, display_name="name")
#renderer = MdRenderer(show_signature=True, show_signature_annotations=True, display_name="name")

# renderer.render(ds_elements['FUNCTION'][15])
# ds_elements['FUNCTION'][15].docstring.parse()

# DocstringSectionParameters: name, annotation, description, default
# from griffe.expressions import Name, Expression
# EL = []#EL.append(d)
# def render_params(self, el: ds.DocstringSectionParameters) -> str:
#   params_str = []
#   for ds_param in el.value:
#     d = ds_param.as_dict()
#     pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
#     sec_md = f"**{pn}** : "
#     if isinstance(pa, Name) or isinstance(pa, Expression):
#       sec_md += f"<span class='type_annotation'> {pa.full}, </span>"
#     else: 
#       sec_md += "" if pa is None or len(str(pa)) == 0 else str(pa)+", "
#     sec_md += f"optional (default={ d.get('value') })" if "value" in d.keys() else "required"
#     sec_md += f"<p> {pd} </p>" #style='margin-top: 10px;margin-left: 2.5em;
#     params_str.append(sec_md)
#   return "\n\n".join(params_str)

# def render_returns(self, el: ds.DocstringSectionReturns) -> str:
#   params_str = []
#   for ds_param in el.value:
#     d = ds_param.as_dict()
#     pn, pa, pd = [d.get(k) for k in ("name", "annotation", "description")]
#     sec_md = f"**{pn}** : "
#     if isinstance(pa, Name) or isinstance(pa, Expression):
#       sec_md += f"<span class='type_annotation'> {pa.full}, </span>"
#     else: 
#       sec_md += "" if pa is None or len(str(pa)) == 0 else str(pa)+", "
#     sec_md += f"<p> {pd} </p>" #style='margin-top: 10px;margin-left: 2.5em;
#     params_str.append(sec_md)
#   return "\n\n".join(params_str)

# #render_overload = MethodType(f, renderer) # doesn't work
# def overload_render(renderer, ds_type, f: Callable):
#   sigs = list(renderer.render.methods.keys())
#   extract_types = lambda T: T.get_types()
#   for sig in sigs:
#     if len(sig.types) > 1 and ds_type in extract_types(sig.types[1]):
#       disp_tup = renderer.render.methods[sig]
#       renderer.render.methods[sig] = f, disp_tup[1]
#       break 

# # from plum import Signature
# # from plum.type import Type
# # import builtins
# # Signature(builtins.object, ds.DocstringSectionAdmonition)
# # list(renderer.render.methods.keys())[14]

# overload_render(renderer, ds.DocstringSectionParameters, render_params)
# overload_render(renderer, ds.DocstringSectionReturns, render_returns)

# key = Signature(Type(builtins.object), ds.DocstringSectionAdmonition)
# key = Signature(Type(builtins.object), ds.DocstringSectionParameters) 
# renderer.render.methods[key]
# renderer.render.methods[key] = Signature(render_params, Type(builtins.object))
