from setuptools import setup, find_packages

setup(
    name='brewDebug',
    version='0.1.0',
    url='',
    author='TurtleP',
    license='MIT',
    description="Parses Atmosphère & Luma3DS Exceptions",
    install_requires=['python-magic'],
    packages=find_packages(),
    entry_points={'console_scripts': ['brewDebug=brewDebug.__main__:main']}
)
