import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_none_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node1, node2)

    def test_prop_eq(self):
        node1 = HTMLNode(children={"href": "https://www.google.com"})
        node2 = HTMLNode(children={"href": "https://www.google.com"})
        self.assertEqual(node1, node2)

    def test_tag_uneq(self):
        node1 = HTMLNode(tag = "", value = "text", children = ["internal", "stuff"])
        node2 = HTMLNode(tag = None, value = "text", children = ["internal", "stuff"])
        self.assertNotEqual(node1, node2)

    def test_prop_uneq(self):
        node1 = HTMLNode(tag = "", value = "text", children = ["internal", "stuff"], props = {})
        node2 = HTMLNode(tag = "", value = "text", children = ["internal", "stuff"])
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()