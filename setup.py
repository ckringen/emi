
from setuptools import setup

setup(
    name = "emi",
    packages = ['src', 'test', 'dependencies', 'benchmarking', "profiling.research.async_examples"],
    include_package_data=True,
)
