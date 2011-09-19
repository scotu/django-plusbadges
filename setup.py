import os
from setuptools import setup, find_packages

setup(
    name='django-plusbadges',
    description='Django app to create Google+ user-badges as embeddable web widgets',
    keywords='django, widget, socialnetworks, simple',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    version="0.3",
    author="Matteo Scotuzzi",
    author_email="matteo.scotuzzi@gmail.com",
    classifiers = ['Framework :: Django',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                   ],
    url="https://github.com/scotu/django-plusbadges",
    license="MIT",
    platforms=["all"],
    install_requires=["pyRFC3339"]
)
