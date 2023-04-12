from setuptools import setup

setup(
    name='ros_database',
    version='0.1.0',
    author='Andrew P. Barrett',
    author_email='andrew.barrett@colorado.edu',
    packages=['ros_database'],
    install_requires=[
        'pytest',
        ],
    license=open('LICENSE').read(),
    description='A package to generate a rain on snow database for the AROSS project',
    long_description=open('README.md').read(),
)
