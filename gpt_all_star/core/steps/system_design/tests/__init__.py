import unittest

from . import test_additional_tasks

# Add the imported module to the list of modules to be discovered by the test runner
test_suite = unittest.TestLoader().loadTestsFromModule(test_additional_tasks)

if __name__ == "__main__":
    unittest.TextTestRunner().run(test_suite)
