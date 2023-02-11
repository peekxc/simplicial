# -*- coding: utf-8 -*-
import os 
import sys
import sysconfig
import distutils.sysconfig
from typing import Any, Dict
from setuptools import setup, Extension, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

# flags = distutils.sysconfig.get_config_var("CFLAGS")

base_path = os.path.dirname(__file__)
compile_flags = list(dict.fromkeys(sysconfig.get_config_var('CFLAGS').split()))
compile_flags += list(dict.fromkeys(sysconfig.get_config_var('CPPFLAGS').split()))
compile_flags += ["-std=c++17", "-Wall", "-Wextra", "-O2", "-Wno-unused-parameter"]
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
  packages=['splex']
)

