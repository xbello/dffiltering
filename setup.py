from setuptools import setup


setup(
    name="dffiltering",
    version="0.1.2",
    description="Command line to filter TSV files.""",
    author_email="xbello@gmail.com",
    packages=["ff"],
    install_requires=[
        "pandas==0.19.1"],
    entry_points={
        "console_scripts": [
            "dff = ff.command.run:run"]})
