from distutils.core import setup, Extension

module = Extension('MyUtils', sources = ["myUtils.cpp"])

setup(name="MyPackage",
    version="1.1",
    description="This is my package for my utils methods",
    author='Giulliano Paz',
    author_email='giulliano94@gmail.com',
    ext_modules = [module])