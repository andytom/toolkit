# Toolkit

[![Build Status](https://travis-ci.org/andytom/toolkit.svg?branch=master)](https://travis-ci.org/andytom/toolkit)

## Overview

Toolkit is a basic collection of small tools that might be useful.

## Running toolkit

You can get toolkit up and running on [localhost:5000](http://localhost:5000/)
using the following instructions. The following assumes you have python,
pip, virtualenv, and virtualenvwrapper installed.

~~~
$ git clone https://github.com/andytom/toolkit.git
$ mkvirtualenv toolkit
$ cd toolkit
$ pip install -r requirements.txt
$ python manage.py runserver
~~~


## Testing

You can run all the test locally using manage.py.

~~~
$ python manage.py runtests
~~~

These tests are also run automatically by [TravisCI](https://travis-ci.org/andytom/toolkit).


## TODO
- [x] Write README and set License
- [x] Write Tests
- [ ] Add logging and Doc strings
 - [ ] app
 - [ ] base64_utils
 - [ ] mkd_preview
 - [ ] table_maker
- [ ] Custom Validators
 - [ ] Table Maker
 - [ ] Base64 Utils

## License
Toolkit is licensed under the BSB license (See LICENSE) for more details.

This doesn't include 3rd Party code in ```app/static/3rd_party```, these files
are licenced under their own licences.
