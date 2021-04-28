from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="psb",
    author="Richard Annand",
    author_email="rj170590@gmail.com",
    url="https://github.com/rj175/pi-status-board",
    project_urls={
        "Bug Tracker": "https://github.com/rj175/pi-status-board/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    version='0.17.0',
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        "AWSIoTPythonSDK",
        "inky",
        "font_fredoka_one",
        "Pillow",
        "boto3",
        "RPi.GPIO"
    ],
    entry_points={
        'console_scripts': [
            'psb = psb.main:shell'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
