# testInit.py
from unittest import TestCase
from operations import operations 

class TestInit(TestCase):
    def setUp(self):
        print("Setting up the test environment")

    def test_prueba1(self):
        self.assertEqual(operations.suma(1,2), 3)
        
    def test_prueba2(self):
        self.assertEqual(operations.suma(2,2), 4)