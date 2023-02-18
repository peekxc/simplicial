# -*- coding: utf-8 -*-
import os 
import sys
import sysconfig
import distutils.sysconfig
from typing import Any, Dict
from setuptools import setup, Extension, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

# flags = distutils.sysconfig.get_config_var("CFLAGS")
print("COMPILER: ", os.environ["CXX"])
# os.environ["CXX"] = "g++"
base_path = os.path.dirname(__file__)
# compile_flags = list(dict.fromkeys(sysconfig.get_config_var('CFLAGS').split()))
# compile_flags += list(dict.fromkeys(sysconfig.get_config_var('CPPFLAGS').split()))
compile_flags = ["-std=c++17", "-Wall", "-Wextra", "-O2", "-Wno-unused-parameter"]
# compile_flags = ["-I/opt/conda/include/python3.10", "-I/opt/conda/include/python3.10", "-Wno-unused-result", "-Wsign-compare", "-march=nocona", "-mtune=haswell", "-ftree-vectorize", "-fPIC", "-fstack-protector-strong", "-fno-plt", "-O3", "-ffunction-sections", "-pipe", "-isystem", "/opt/conda/include", "-fdebug-prefix-map=/croot/python-split_1669298683653/work=/usr/local/src/conda/python-3.10.8", "-fdebug-prefix-map=/opt/conda=/usr/local/src/conda-prefix", "-fuse-linker-plugin", "-ffat-lto-objects", "-flto-partition=none", "-flto", "-DNDEBUG", "-fwrapv", "-O3", "-Wall", "-L/opt/conda/lib/python3.10/config-3.10-x86_64-linux-gnu", "-L/opt/conda/lib", "-lcrypt", "-lpthread", "-ldl", "-lutil", "-lm", "-lm"]
# "-lstdc++", "-lpython3.9","-L/opt/conda/lib/python3.10/config-3.10-x86_64-linux-gnu", "-L/opt/conda/lib", "-lcrypt", "-lpthread", "-ldl",  "-lutil", "-lm", "-ld"]
print(f"COMPILER FLAGS: { str(compile_flags) }")

ext_modules = [
  Pybind11Extension(
    'splex.complexes._simplextree', 
    sources = ['src/splex/complexes/simplextree_module.cpp'], 
    include_dirs=[
      'extern/pybind11/include',
      'src/splex/include'
    ], 
    extra_compile_args=compile_flags,
    language='c++17'
  ), 
   Pybind11Extension(
    '_union_find', 
    sources = ['src/splex/UnionFind.cpp'], 
    include_dirs=[
      'extern/pybind11/include'
    ], 
    extra_compile_args=compile_flags,
    language='c++17'
  )
]

setup(
  name="splex",
  author="Matt Piekenbrock",
  author_email="matt.piekenbrock@gmail.com",
  description="Package for manipulating simplicial complexes",
  long_description="",
  ext_modules=ext_modules,
  cmdclass={'build_ext': build_ext},
  zip_safe=False, # needed for platform-specific wheel 
  python_requires=">=3.8",
  package_dir={'': 'src'}, # < root >/src/* contains packages
  packages=['splex', 'splex.complexes', 'splex.filtrations']
)

