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
    tests = unittest.TestLoader().discover('./app')
    results = unittest.TextTestRunner().run(tests)


if __name__ == "__main__":
    manager.run()
