from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize('tool.pyx'),
    extra_compile_args=['-stdlib=libc++', '-I /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/numpy/core/include']
)