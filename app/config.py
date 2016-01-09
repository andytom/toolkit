# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~
    Configuration for Toolkit.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
import os

# See the Flask docs for how to generate a good secret key
# http://flask.pocoo.org/docs/0.10/quickstart/#sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')
