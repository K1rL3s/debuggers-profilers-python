# python c_capi_setup.py build_ext --inplace --compiler=mingw32
from setuptools import setup, Extension

module = Extension(name='integration', sources=['c_capi.c'])

setup(
    name='integration',
    version='1.0',
    description='A simple Python C extension module',
    ext_modules=[module]
)