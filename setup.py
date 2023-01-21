# -*- coding: utf-8 -*-
import os 
import sysconfig
import distutils.sysconfig
from typing import Any, Dict
from setuptools import setup, Extension, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

base_path = os.path.dirname(__file__)
extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
extra_compile_args += ["-std=c++17", "-Wall", "-Wextra", "-O2", "-Wno-unused-parameter"]

flags = distutils.sysconfig.get_config_var("CFLAGS")
print(f"COMPILER FLAGS: { str(flags) }")

ext_modules = [
  Pybind11Extension(
    '_simplextree', 
    sources = ['src/simplicial/simplextree_module.cpp'], 
    include_dirs=[
      '/Users/mpiekenbrock/simplicial/extern/pybind11/include',
      '/Users/mpiekenbrock/simplicial/src/simplicial/include'
    ], 
    extra_compile_args=extra_compile_args,
    language='c++17', 
    cxx_std=1
  )
]

setup(
  name="simplicial",
  author="Matt Piekenbrock",
  author_email="matt.piekenbrock@gmail.com",
  description="Persistent Betti Signatures",
  long_description="",
  ext_modules=ext_modules,
  cmdclass={'build_ext': build_ext},
  zip_safe=False, # needed for platform-specific wheel 
  python_requires=">=3.8",
  package_dir={'': 'src'}, # < root >/src/* contains packages
  packages=['simplicial'],
  # package_data={'pbsig': ['data/*.bsp', 'data/*.txt', 'data/*.csv']},
  # cmake_install_dir='src/pbsig'
  #cmake_args=['-DSOME_FEATURE:BOOL=OFF']
)
# package_dir = \
# {'': 'src'}

# packages = \
# ['set_cover', 'set_cover.sc_ext']

# package_data = \
# {'': ['*'],
#  'set_cover.sc_ext': ['extern/pybind11/*',
#                       'extern/pybind11/detail/*',
#                       'extern/pybind11/stl/*']}

# setup_kwargs = {
#     'name': 'set-cover',
#     'version': '0.1.0',
#     'description': 'My Package with C++ Extensions',
#     'long_description': None,
#     'author': 'Matt Piekenbrock',
#     'author_email': None,
#     'maintainer': None,
#     'maintainer_email': None,
#     'url': None,
#     'package_dir': package_dir,
#     'packages': packages,
#     'package_data': package_data,
# }
# from build import *
# build(setup_kwargs)

# setup(**setup_kwargs)
