# -*- coding: utf-8 -*-
"""
    mkd_preview
    ~~~~~~~~~~~
    Blueprint for live markdown preview.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, render_template, g, current_app


mkd_preview = Blueprint('mkd_preview', __name__, template_folder='templates')


EXAMPLE_MARKDOWN_TEXT = """# Title

Some example text

## Sub Title

Some code

~~~
for i in range(10):
    print i
~~~

## Another Sub Title

A link to the [Github Flavoured Markdown documentaion](https://help.github.com/articles/github-flavored-markdown/)."""


@mkd_preview.route('/')
def index():
    """Index page for mkd_preview.

       :returns: The rendered index template.
    """
    current_app.logger.debug('Rendering mkd_preview index page')
    return render_template('mkd_preview/index.html',
                           content=EXAMPLE_MARKDOWN_TEXT)
