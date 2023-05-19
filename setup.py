from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='references_parser',
    packages=setuptools.find_packages(),
    version='1.2.0',
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
    ], 
    install_requires=[
        "beautifulsoup4==4.12.2",
        "bibtexparser==1.4.0",
        "click==8.1.3",
        "duckpy==3.2.0",
        "Requests==2.30.0",
        "pydantic==1.10.2",
        "tqdm==4.64.1"
    ],
    entry_points={
        'console_scripts': [
            'references_parser=references_parser.cli:main'
        ]
    }
)
