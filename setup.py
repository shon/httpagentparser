from setuptools import setup, find_packages

for line in open('httpagentparser/__init__.py'):
    if line.startswith('__version__'):
        version = line.split('=')[-1].strip()[1:-1]
        break

setup(
    name='httpagentparser',
    version=version,
    url="http://shon.github.com/httpagentparser",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
        ],
    include_package_data=True,
    description='Extracts OS Browser etc information from http user agent string',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    author='Shekhar Tiwatne',
    author_email='pythonic@gmail.com',
    license="http://www.opensource.org/licenses/mit-license.php",
    test_suite="tests",
    )

