from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='references_parser',
    packages=setuptools.find_packages(),
    version='0.2.2',
    description="Tool for parsing bibtex in ssau's format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mukhin Artem',
    author_email='artemmukhinssau@gmail.com',
    url='https://github.com/Banayaki/ReferencesParser',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ], install_requires=[
        'bibtexparser~=1.2.0'
    ]
)
