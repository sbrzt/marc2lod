import unittest, parse

class TestParse(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(parse.clean_text("Book :"), "Book")
        self.assertEqual(parse.clean_text("Mike & Johnny. "), "Mike & Johnny")

if __name__ == '__main__':
    unittest.main()