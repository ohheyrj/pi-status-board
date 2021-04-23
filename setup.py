from setuptools import setup, find_packages

setup(
    name="psb",
    version='0.12.dev',
    packages=find_packages(),
    install_requires=[
        "AWSIoTPythonSDK",
        "inky",
        "font_fredoka_one",
        "Pillow",
        "boto3"
    ],
    entry_points={
        'console_scripts': [
            'psb = psb.main:shell'
        ]
    }
)
