from setuptools import setup


setup(
    name="dffiltering",
    version="0.1.4",
    description="Command line to filter TSV files.""",
    author_email="xbello@gmail.com",
    packages=["dffiltering.ff", "dffiltering.command"],
    install_requires=[
        "pandas==0.19.1"],
    entry_points={
        "console_scripts": [
            "dff = dffiltering.command.run:run"]})
