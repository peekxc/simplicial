# -*- coding: utf-8 -*-
import os 
import sys
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
    sources = ['src/splex/simplextree_module.cpp'], 
    include_dirs=[
      'extern/pybind11/include',
      'src/splex/include'
    ], 
    extra_compile_args=extra_compile_args,
    language='c++17', 
    cxx_std=1
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

