from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="azure-graph-toolkit",
    version="1.0.9",
    author="Ivano Dibenedetto",
    author_email="ivano.dibenedetto7@gmail.com",
    description="Lightweight python library for easily managing Azure AD (Entra ID) users and groups through the Graph API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ivanodib/azure-graph-toolkit",
    packages=find_packages(),   
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)