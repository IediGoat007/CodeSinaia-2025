import unittest
from roman_converter import roman_converter

class TestInvalidInput(unittest.TestCase):
    # ======== Step 1 ======== no input, return None
    def test_no_input(self):
        self.assertEqual(roman_converter(None), None)

<<<<<<< HEAD
    def test_minimum(self):
        self.assertEqual(roman_converter(0), None)

    def test_maximum(self):
        self.assertEqual(roman_converter(4000), None)

    def test_one(self):
        self.assertEqual(roman_converter(1), "I")

    def test_five(self):
        self.assertEqual(roman_converter(5), "V")
    
    def test_ten(self):
        self.assertEqual(roman_converter(10), "X")

    def test_fifty(self):
        self.assertEqual(roman_converter(50), "L")

    def test_hundred(self):
        self.assertEqual(roman_converter(100), "C")

    def test_five_hundred(self):
        self.assertEqual(roman_converter(500), "D") 

    def test_one_thousand(self):
        self.assertEqual(roman_converter(1000), "M")
=======
    def test_str(self):
        self.assertEqual(roman_converter('schaorma'), None)

    def test_dec(self):
        self.assertEqual(roman_converter(3.14), None)

    def test_min(self):
        self.assertEqual(roman_converter(0), None)

    def test_max(self):
        self.assertEqual(roman_converter(4000), None)

    def test_one(self):
        self.assertEqual(roman_converter(1), 'I')

    def test_two(self):
        self.assertEqual(roman_converter(2), 'II')

    def test_four(self):
        self.assertEqual(roman_converter(4), 'IIII')

    def test_five(self):
        self.assertEqual(roman_converter(5), 'V')
    
    def test_six(self):
        self.assertEqual(roman_converter(6), 'VI')
    
    def test_ten(self):
        self.assertEqual(roman_converter(10), 'X')
>>>>>>> 9acbaf18bb99f7d6895d8d125fdfcba3807b2a33
