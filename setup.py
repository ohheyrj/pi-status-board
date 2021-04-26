from setuptools import setup, find_packages

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
        "Natural Language :: English"
    ],
    version='0.16.0',
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
    }
)
