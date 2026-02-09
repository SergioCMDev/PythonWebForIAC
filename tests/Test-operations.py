# testInit.py
# import unittest
from unittest import TestCase
import operations

class TestInit(TestCase):
    def setUp(self):
        print("Setting up the test environment")

    def test_prueba1(self):
        self.assertEqual(operations.suma(1,2), 3)
    