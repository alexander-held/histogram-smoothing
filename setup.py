from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="histogram-smoothing",
    version="0.0.1",
    author="Alexander Held",
    description="utilities for histogram smoothing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD 3-Clause",
    url="https://github.com/alexander-held/histogram-smoothing",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy"],
)
