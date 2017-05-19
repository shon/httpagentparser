from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    """ Running tox from setup.py.
    See:
    https://testrun.org/tox/latest/example/basic.html#integration-with-setuptools-distribute-test-commands
    """
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def __init__(self, dist, **kw):
        TestCommand.__init__(self, dist, **kw)
        self.tox_args = None
        self.test_args = []
        self.test_suite = True

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex

        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


for line in open('httpagentparser/__init__.py'):
    if line.startswith('__version__'):
        version = line.split('=')[-1].strip()[1:-1]
        break

setup(
    name='httpagentparser',
    version=version,
    url="http://shon.github.com/httpagentparser",
    classifiers=[
        'Programming Language :: Python :: 2.7',
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
    tests_require=['tox'],
    cmdclass={'test': Tox},
    )

