from setuptools import setup, find_packages

setup(
    name='httpagentparser',
    version='1.0.1',
    description='Extracts OS Browser etc information from http user agent string',
    long_description=file("README.rst").read(),
    packages=find_packages(),
    author='Shekhar Tiwatne',
    author_email='pythonic@gmail.com',
    url="http://flavors.me/shon",
    license="http://www.opensource.org/licenses/mit-license.php",
    )

