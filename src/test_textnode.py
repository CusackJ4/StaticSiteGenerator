import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url_none(self):
        node3 = TextNode("Node text", TextType.NORMAL, None)
        node4 = TextNode("Node text", TextType.NORMAL)
        self.assertEqual(node3, node4)

    def test_url_eq(self):
        node4 = TextNode("Node text", TextType.NORMAL, "geek.com")
        node5 = TextNode("Node text", TextType.NORMAL, "geek.com")
        self.assertEqual(node4, node5)

    def test_text_ineq(self):
        node6 = TextNode("Node texts", TextType.NORMAL, "geek.com")
        node7 = TextNode("Node text", TextType.NORMAL, "geek.com")
        self.assertNotEqual(node6, node7)


if __name__ == "__main__":
    unittest.main()
