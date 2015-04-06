# -*- coding: utf-8 -*-
"""
    toolkit
    ~~~~~~~
    Toolkit is a basic collection of small tools that might be useful.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
#-----------------------------------------------------------------------------#
# Setup
#-----------------------------------------------------------------------------#
from flask import Flask, render_template, url_for, g
from base64_utils import base64_utils
from table_maker import table_maker
from mkd_preview import mkd_preview

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(base64_utils, url_prefix='/base64_utils')
app.register_blueprint(table_maker, url_prefix='/table_maker')
app.register_blueprint(mkd_preview, url_prefix='/mkd_preview')


if not app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('Application started')


#-----------------------------------------------------------------------------#
# Hooks
#-----------------------------------------------------------------------------#
@app.before_request
def before_request():
    """Pre-request hook. Set the g.TOOLS dict to the each of the tools that
       have been set up.
    """
    g.TOOLS = {
        'Base64 Utilities': {
            'url': url_for('base64_utils.index'),
            'description': "Decode Base64 encoded files."
        },
        'Table Maker': {
            'url': url_for('table_maker.index'),
            'description': "Convert CSV strings into ASCII tables."
        },
        'Markdown Preview': {
            'url': url_for('mkd_preview.index'),
            'description': "Live Preview of Markdown text."
        }
    }


#-----------------------------------------------------------------------------#
# Route
#-----------------------------------------------------------------------------#
@app.route('/')
def index():
    """Index Page

        :returns: The rendered index template.
    """
    app.logger.debug('Rendering index page')
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    """Generic 404 error page.

        :param error: An exception from the error.

        :returns: The rendered 404 error template.
    """
    app.logger.debug('Rendering 404 page')
    return render_template('404.html'), 404
