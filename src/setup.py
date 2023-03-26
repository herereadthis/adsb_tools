from pathlib import Path
from setuptools import setup
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='adsb_tools',
    version='0.1.33',
    packages=['adsb_tools'],
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'pytz',
        'timezonefinder'
    ],
    author='herereadthis',
    author_email='herereadthis.github@gmail.com',
    description='Various tools for handling ADS-B data coming from Dump1090 messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/herereadthis/adsb_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
