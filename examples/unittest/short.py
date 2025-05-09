import unittest

class TestDict(unittest.TestCase):
    def setUp(self):
        self.dictionary = {}

    def test_dict(self):
        self.assertEqual(len(self.dictionary), 0)
        self.dictionary["key"] = "value"
        self.assertEqual(self.dictionary["key"], "value")
        self.assertEqual(len(self.dictionary), 1)
        del self.dictionary["key"]
        with self.assertRaises(KeyError):
            self.dictionary["key"]

if __name__ == "__main__":
    unittest.main()