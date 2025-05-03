# python cython_setup.py build_ext --inplace --compiler=mingw32
from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

extensions = [
    Extension(
        "cython_file",
        sources=["cython_file.pyx", "simple.c"],
        include_dirs=["."],
    )
]

setup(
    name="cython_integration",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)