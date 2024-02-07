"""
This file is setuptools.
"""
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', encoding='utf-8') as requirements_file:
    requirements_list = requirements_file.read().strip().split("\n")

setup(
    name='craftsperson-env',
    version='1.0.0',
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Celal Akçelik',
    author_email='celalakcelikk@gmail.com',
    url='https://github.com/celalakcelikk/craftsperson-env',
    python_requires='>=3.8',
    install_requires=requirements_list,
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Production/Stable",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python",
    ],
    keywords=[
        "environment",
        "PyYAML",
        "yaml"
        "toml",
        "env",
        "json",
        "xml",
        "xmltodict",
        "Python",
        "projects",
        "Config",
        "package",
        "packaging"]

)
