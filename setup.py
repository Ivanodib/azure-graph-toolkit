from setuptools import setup, find_packages

setup(
    name='azure-graph-helper',
    version='1.0',
    description='Python library that help to automate Azure operations.',
    author='Ivano Dibenedetto',
    author_email='ivano.dibenedetto7@gmail.com',
    install_requires=[
    'msal',
    ],
    packages=find_packages(),
)