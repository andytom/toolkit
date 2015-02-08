from flask import Blueprint, render_template, g


mkd_preview = Blueprint('mkd_preview', __name__, template_folder='templates')


@mkd_preview.before_request
def before_request():
    g.title = 'Markdown Preview'


@mkd_preview.route('/')
def index():
    return render_template('mkd_preview/index.html')
