
from distutils.core import setup

setup(
    name = "emi",
    author="Chad Kringen",
    packages = ['src', 'third-party', "profiling.research.async_examples"],
    include_package_data=True,
)
