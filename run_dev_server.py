#-----------------------------------------------------------------------------#
# Set up the Dev Server
#-----------------------------------------------------------------------------#
from app import app

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'Testing'
    app.run('0.0.0.0')
