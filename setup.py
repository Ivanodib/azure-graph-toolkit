from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="azure-graph-helper",
    version="1.0.1.1",
    author="Ivano Dibenedetto",
    author_email="ivano.dibenedetto7@gmail.com",
    description="Python library to manage Azure AD (Entra ID) user groups easily through Graph API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ivanodib/azure-graph-helper",
    packages=find_packages(),   
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)