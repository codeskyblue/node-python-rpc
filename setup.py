# coding: utf-8
#

__version__ = '0.0.1'

from setuptools import setup, find_packages


setup(
      name='nodepythonrpc',
      version=__version__,
      description='bridge between node and python',
      author='codeskyblue',
      author_email='codeskyblue@gmail.com',

      packages = find_packages(),
      include_package_data=True,
      package_data={},
      install_requires=[
          'tornado>=4.1',
          ],
      )
