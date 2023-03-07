from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='adsb_tools',
    version='0.1.2',
    packages=['adsb_tools.distance'],
    entry_points={
        'console_scripts': [
            'adsb_tools=adsb_tools.distance.__main__:main'
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'typing'
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
