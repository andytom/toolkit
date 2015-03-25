import unittest

def run_all_tests():
    tests = unittest.TestLoader().discover('./app')
    results = unittest.TextTestRunner().run(tests)


if __name__ == '__main__':
    run_all_tests()
