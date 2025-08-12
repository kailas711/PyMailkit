import warnings
from setuptools import setup, find_packages

# Suppress all warnings
warnings.filterwarnings("ignore")

# Tell the build backend where the package files are
setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)