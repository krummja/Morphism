from setuptools import find_packages, setup
import sys

install_requires = []
if sys.version_info < (3, 5):
    install_requires.append('typing')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='morphism',
    version='0.0.1',
    author='Jonathan Crum',
    author_email="crumja4@gmail.com",
    url="https://github.com/krummja/Morphism",
    license='MIT',
    description='A little library for 2D game development in Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['morphism']),
    install_requires=install_requires,
    setup_requires=[],
    tests_require=['pytest==6.2.1'],
    test_suite='tests',
    python_requires='>=3.8.5',
    )
