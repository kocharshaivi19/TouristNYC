import os
from setuptools import setup

requires = (
    'Jinja2',
	'Werkzeug',
	'certifi',
	'chardet',
	'distribute',
	'gunicorn',
	'requests',
	'urllib3',
    'itsdangerous>=0.21',
    'click>=2.0',
)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tourist-nyc",
    version = "0.0.1",
    author = "Shaivi Kochar",
    author_email = "sk6435@nyu.edu",
    description = ("awesome"),
    license = "BSD",
    keywords = "Tourist Guide to NYC",
    packages=['tourist-nyc',],
    install_requires=requires,
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
        [console_scripts]
        flask=flask.cli:main
    '''
)
