import unittest
from site_copier import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_exception(self):
        contents = "This is a string without any markdown formatting or newlines."
        md = "#"
        with self.assertRaises(Exception):
            extract_title(md, contents)
    def test_partial_h1_match(self):
        contents = "Line One\nLineTwo\n# Line Three and a bit.\nLine Four"
        md = "# Line Three"
        self.assertEqual(extract_title(md, contents), "Line Three and a bit.")
    def test_he2_fails(self):
        contents = "Line One\n## LineTwo\n# Line Three and a bit.\nLine Four"
        md = "# Line Three"
        self.assertEqual(extract_title(md, contents), "Line Three and a bit.")



if __name__ == "__main__":
    unittest.main()