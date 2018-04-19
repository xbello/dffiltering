from setuptools import setup
from dffiltering.ff import _version


setup(
    name="dffiltering",
    version=_version.__version__,
    description="Command line to filter TSV files.""",
    author_email="xbello@gmail.com",
    packages=["dffiltering.ff", "dffiltering.command"],
    install_requires=[
        "pandas==0.19.2",
        "colorama==0.3.9"],
    entry_points={
        "console_scripts": [
            "dff = dffiltering.command.run:run"]})
