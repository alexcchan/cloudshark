#!/usr/bin/python

from distutils.core import setup

setup(
	# Basic package information.
	name = 'cloudshark',
	version = '0.0.0',
	packages = ['cloudshark'],
	include_package_data = True,
	install_requires = ['httplib2'],
	url = 'https://github.com/alexcchan/cloudshark/tree/master',
	keywords = 'cloudshark api',
	description = 'Cloudshark API Wrapper for Python',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet'
	],
)


