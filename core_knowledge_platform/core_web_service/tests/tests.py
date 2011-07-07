"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest

import view_tests
suite = unittest.TestLoader().loadTestsFromTestCase(view_tests)
unittest.TextTestRunner().run(suite)

