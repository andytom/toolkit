from flask import Blueprint, render_template, g


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


@mkd_preview.before_request
def before_request():
    g.title = 'Markdown Preview'


@mkd_preview.route('/')
def index():
    return render_template('mkd_preview/index.html',
                           content=EXAMPLE_MARKDOWN_TEXT)
