import unittest

from gpt_all_star.tests.test_project import TestProject

# Import the new unit tests from test_project.py
# Add the new unit tests to the test suite
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestProject))

# Run the test suite to verify that all tests pass
if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite)
