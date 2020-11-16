from setuptools import setup, find_packages

setup(
    name='brewDebug',
    version='0.3.0',
    url='https://github.com/TurtleP/brewDebug',
    author='TurtleP',
    license='MIT',
    description="Parses Atmosphère & Luma3DS Exceptions",
    install_requires=['python-magic', "toml"],
    packages=find_packages(),
    entry_points={'console_scripts': ['brewDebug=brewDebug.__main__:main']}
)
