from setuptools import setup
from setuptools import find_packages

required = [
    "numpy",
    "pandas",
    "pydocstyle",
    "pytest",
    "pytest-cov",
    "pylint",
    "delphi-utils",
    "imap-tools",
    "xlrd==1.2.0",
    "covidcast"
]

setup(
    name="quidel",
    version="0.1.0",
    description="Indicators Pulled from datadrop email account",
    author="",
    author_email="",
    url="https://github.com/cmu-delphi/covidcast-indicators",
    install_requires=required,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
)
