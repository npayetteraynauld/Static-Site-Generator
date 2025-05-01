import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_valid_title(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_title_with_extra_spaces(self):
        self.assertEqual(extract_title("   #    Title with spaces   "), "Title with spaces")

    def test_title_with_special_chars(self):
        self.assertEqual(extract_title("# Welcome to *Markdown*!"), "Welcome to *Markdown*!")

    def test_no_title(self):
        with self.assertRaises(Exception):
            extract_title("## Not an H1")

    def test_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_no_hash(self):
        with self.assertRaises(Exception):
            extract_title("Just text")

if __name__ == "__main__":
    unittest.main()
