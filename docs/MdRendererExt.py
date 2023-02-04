from quartodoc import MdRenderer
from griffe import dataclasses as dc
from griffe.docstrings import dataclasses as ds
from plum import dispatch
from tabulate import tabulate

GLOBAL_TABS = []

# class MdRendererNumpyStyle(MdRenderer):
#   style = "markdown_numpy"

#   @dispatch
#   def render(self, el: ds.DocstringSectionParameters):
#     rows = list(map(self.render, el.value))
#     # GLOBAL_TABS.append(el)
#     header = ["Name", "Type", "Description", "Default"]
#     GLOBAL_TABS.append([rows, header])
#     # return tabulate(rows, header, tablefmt="github")
#     params_str = []
#     for param_name, param_type, param_descr, default_val in rows:
#       if len(param_type) > 0:
#         params_str.append(f"{param_name} : _{param_type}_ (Default: {default_val}) \n\n &nbsp;&nbsp;&nbsp;&nbsp; <p> {param_descr} </p>")
#       else:
#         params_str.append(f"{param_name} : (Default: {default_val}) \n\n &nbsp;&nbsp;&nbsp;&nbsp; <p> {param_descr} </p>")
#     return "\n\n".join(params_str)

  # @dispatch
  # def render(self, el: dc.Parameter):
  #   # TODO: missing annotation
  #   splats = {dc.ParameterKind.var_keyword, dc.ParameterKind.var_positional}
  #   has_default = el.default and el.kind not in splats

  #   annotation = self._render_annotation(el.annotation)
  #   print("annotation" + annotation)
  #   if self.show_signature_annotations:
  #     if annotation and has_default:
  #       return f"{el.name}: {el.annotation} = {el.default}"
  #     elif annotation:
  #       return f"{el.name}: {el.annotation}"
  #   elif has_default:
  #     return f"{el.name}={el.default}"
  #   return el.name
