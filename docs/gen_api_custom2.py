import yaml
import quartodoc
from quartodoc import Builder, preview, blueprint, collect, MdRenderer

## Config 
cfg = yaml.safe_load(open("_quarto.yml", "r"))

## Builder 
builder = Builder.from_quarto_config(cfg)
print(preview(builder.layout))




## Simplex Tree
preview(builder.layout.sections[0])
bp = blueprint(builder.layout)

from splex import complexes

preview(bp, max_depth=5)
