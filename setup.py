from setuptools import setup, find_packages

setup(
    name='httpagentparser',
    version='1.5.1',
    url="https://github.com/shon/httpagentparser",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
        ],
    include_package_data=True,
    description='Extracts OS Browser etc information from http user agent string',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    author='Shekhar Tiwatne',
    author_email='pythonic@gmail.com',
    license="http://www.opensource.org/licenses/mit-license.php",
    test_suite="tests",
    )

