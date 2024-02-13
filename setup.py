from setuptools import setup, find_packages
setup(
name='mypackage',
version='0.1.0',
package_dir={"": "src"},
author='Gabe',
author_email='gunderwood@labelbox.com',
description='module of classes to assist on getting model results to labelbox',
packages=find_packages(where="src"),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)