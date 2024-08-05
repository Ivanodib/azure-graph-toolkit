from setuptools import setup, find_packages

setup(
    name='azure-graph-helper',
    version='1.0',
    description='Python library to manage Azure AD (Entra ID) user groups easily through Graph API.',
    author='Ivano Dibenedetto',
    author_email='ivano.dibenedetto7@gmail.com',
    install_requires=[
    'msal',
    ],
    packages=find_packages(),
)