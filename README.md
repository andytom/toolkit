# Toolkit

[![Build Status](https://travis-ci.org/andytom/toolkit.svg?branch=master)](https://travis-ci.org/andytom/toolkit)

## Overview

Toolkit is a basic collection of small tools that might be useful.

## Running toolkit

You can get toolkit up and running on [localhost:5000](http://localhost:5000/)
using the following instructions.

~~~
$ git clone https://github.com/andytom/toolkit.git
$ mkvirtualenv toolkit
$ cd toolkit
$ pip install -r requirements.txt
$ python manage.py runserver
~~~


## Testing

You can run all the test locally using.

~~~
$ python manage.py runtests
~~~

These tests are also run by [TravisCI](https://travis-ci.org/andytom/toolkit).


## TODO
- [ ] Write README
- [ ] Write Tests
 - [x] app
 - [ ] base64_utils
 - [x] mkd_preview
 - [x] table_maker
- [ ] Custom Validators
 - [ ] Table Maker
 - [ ] Base64 Utils

## License
