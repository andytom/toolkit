#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~
    Mangement commands for Toolkit.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import unittest
from flask.ext.script import Manager, Server
from app import app


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Testing'


manager = Manager(app)


server = Server(host='0.0.0.0')
manager.add_command("runserver", server)


@manager.command
def runtests():
    """Runs all the tests"""
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(parent_dir, 'app')
    tests = unittest.TestLoader().discover(app_dir)
    results = unittest.TextTestRunner(verbosity=2).run(tests)

    ret = not results.wasSuccessful()
    sys.exit(ret)


if __name__ == "__main__":
    manager.run()
