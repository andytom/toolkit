import unittest


tests = unittest.TestLoader().discover('./app')
results = unittest.TextTestRunner().run(tests)
