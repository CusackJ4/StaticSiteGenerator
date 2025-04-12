import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url_none(self):
        node3 = TextNode("Node text", TextType.TEXT, None)
        node4 = TextNode("Node text", TextType.TEXT)
        self.assertEqual(node3, node4)

    def test_url_eq(self):
        node4 = TextNode("Node text", TextType.TEXT, "geek.com")
        node5 = TextNode("Node text", TextType.TEXT, "geek.com")
        self.assertEqual(node4, node5)

    def test_text_ineq(self):
        node6 = TextNode("Node texts", TextType.TEXT, "geek.com")
        node7 = TextNode("Node text", TextType.TEXT, "geek.com")
        self.assertNotEqual(node6, node7)

class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(len(html_node.props), 2)
        self.assertEqual(html_node.props["alt"], node.text)
    def test_two_uneq(self):
        node1 = TextNode("This is a text node", TextType.LINK)
        html_node1 = text_node_to_html_node(node1)
        node2 = TextNode("This is a text node", TextType.CODE)
        html_node2 = text_node_to_html_node(node2)
        self.assertNotEqual(html_node1.tag, html_node2.tag)
        self.assertNotEqual(html_node1.props, html_node2.props)

    




if __name__ == "__main__":
    unittest.main()
