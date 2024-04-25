from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in qoala/__init__.py
from qoala import __version__ as version

setup(
	name="qoala",
	version=version,
	description="insurance technology company",
	author="safvanhussain",
	author_email="safvanph41@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
