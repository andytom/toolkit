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


#-----------------------------------------------------------------------------#
# Hooks
#-----------------------------------------------------------------------------#
@app.before_request
def before_request():
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
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
