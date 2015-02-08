import os

# See the Flask docs for how to generate a good secret key
# http://flask.pocoo.org/docs/0.10/quickstart/#sessions
SECRET_KEY = os.environ.get('SECRET_KEY')
