# ---
# jupyter: python3
# ---

from griffe import dataclasses as dc
from griffe.docstrings import dataclasses as ds
from griffe.loader import GriffeLoader
from griffe.docstrings.parsers import Parser, parse
from pathlib import Path
from plum import dispatch
from quartodoc import MdRenderer

griffe = GriffeLoader(docstring_parser=Parser("google"))
mod = griffe.load_module("simplicial")
renderer = MdRenderer(show_signature=True, show_signature_annotations=True, display_name="name")
auto_summaries = {}
class_summaries = {}

def filter_invalid_ds(docstrings):
  if docstrings is None: return []
  parsed = parse(docstrings, Parser.google)
  parsed = list(filter(lambda dso: type(dso) != ds.DocstringSectionAdmonition, parsed))
  return parsed

## TODO: Create a new renderer! 
# class MdRendererExtended(MdRenderer):

class AutoSummary:
  def __init__(self, dir_name: str):
    self.dir_name = dir_name

  @staticmethod
  def full_name(el):
    # print(f"{el.parent.name}.{el.name}")
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

  @dispatch
  def visit(self, el: dc.Module):
    print(f"MOD: {el.canonical_path}")
    for name, class_ in el.classes.items():
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
    class_summaries[el.name] = el
    parsed = filter_invalid_ds(el.docstring)
    class_summary = '\n\n'.join([renderer.render(p) for p in parsed])
    auto_summaries.setdefault(el.name, [f"# {el.name}"]).append(class_summary)
    for name, method in el.members.items():
      self.visit(method)

  @dispatch
  def visit(self, el: dc.Alias):
    return None

  @dispatch
  def visit(self, el: dc.Function):
    if el.name.startswith("_"):
      return
    full_name = self.full_name(el)
    print(f"FUNCTION: {full_name}")
    
    ## Accumulate the auto summaries per basename
    auto_summaries.setdefault(self.parent_name(el), []).append(renderer.render(el))
    

  @dispatch
  def visit(self, el: dc.Attribute):
    if el.name.startswith("_"):
      return

    # a class attribute
    print(f"ATTR: {self.full_name(el)}")

## Create the files
output_dir = "API"
auto = AutoSummary(output_dir)
auto.visit(mod)
p_root = Path(auto.dir_name)
p_root.mkdir(exist_ok=True)
for fn in auto_summaries.keys():
  p_func = p_root / f"{fn}.md"
  p_func.write_text("\n\n --- \n\n".join(auto_summaries[fn]))


