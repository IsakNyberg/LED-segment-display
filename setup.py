#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="max7219_drivers_pi",
    version="0.0.1",
    author="Isak Nyberg",
    description="Drivers for the MAX7219 board.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IsakNyberg/max7219_drivers_pi",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
