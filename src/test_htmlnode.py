import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_children(self):
        node = LeafNode("p", "five")
        with self.assertRaises(AttributeError):
            node.__setattr__("children", "five")

    def test_props_eq(self):
        node1 = LeafNode("p", "Hello, world!", props=None)
        node2 = LeafNode("p", "Hello, world!", )
        self.assertEqual(node1, node2)

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "a header!")
        self.assertEqual(node.to_html(), "<h1>a header!</h1>")

    def test_to_html_property(self):
        node = LeafNode("tr", "table row stuff", props = {"target": "_blank"})
        self.assertEqual(node.to_html(), "<tr target=\"_blank\">table row stuff</tr>")
            
class TestParentNode(unittest.TestCase): 
    def test_conversion_success(self):
        node1 = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node2 = LeafNode("span", "child 2")
        child_node1 = LeafNode("span", "child 1")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child 1</span><span>child 2</span></div>")

    def test_to_html_with_props(self):
        child_node1 = LeafNode("span", "child 1")
        parent_node = ParentNode("div", [child_node1], {
                        "href": "https://www.google.com", "target": "_blank", "id": "35",})
        self.assertEqual(parent_node.to_html(), 
                         "<div href=\"https://www.google.com\" target=\"_blank\" id=\"35\"><span>child 1</span></div>")
    


if __name__ == "__main__":
    unittest.main()