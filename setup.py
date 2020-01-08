# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "ingram_data_services", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

# with open('README.rst', 'r', 'utf-8') as f:
#     readme = f.read()
# with open('CHANGELOG.rst', 'r', 'utf-8') as f:
#     history = f.read()

setup(
    name=about["__pip_package_name__"],
    version=about["__version__"],
    description=about["__description__"],
    # long_description=readme + '\n\n' + history,
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    keywords=about["__keywords__"],
    license=about["__license__"],
    include_package_data=True,
    install_requires=about["__install_requires__"],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
    # python_requires=(">2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, " "!=3.5.*"),
    entry_points={"console_scripts": ["ingram-data-services = ingram_data_services.ingram:main"]},
)
