from setuptools import setup

setup(
    name='adsb_tools',
    version='0.1.0',
    packages=['adsb_tools.distance'],
    entry_points={
        'console_scripts': [
            'adsb_tools=adsb_tools.distance.__main__:main'
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'typing',
        'math'
    ],
    author='herereadthis',
    author_email='herereadthis.github@gmail.com',
    description='Various tools for handling ADS-B data coming from Dump1090 messages',
    url='https://github.com/herereadthis/adsb_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
