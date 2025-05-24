from setuptools import setup, find_packages

setup(
    name="trajectory_simulation",
    version="0.1",
    packages=find_packages(),
    package_dir={'': '.'},  # Bu satırı ekleyin
)