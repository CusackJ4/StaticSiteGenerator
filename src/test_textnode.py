import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_functions import *


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

class Test_split_nodes(unittest.TestCase):
    def test_missing_delim(self):
        node = [TextNode("This is text with a `code block word", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes=node, delimiter="`", text_type=TextType.CODE)
    def test_italics(self):
        node = [TextNode("TEST 3: This _is text_ with two _italics_ sections", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes=node, delimiter="_", text_type=TextType.ITALIC) # returns list of lists
        self.assertEqual(result[1].text_type, result[3].text_type, TextType.ITALIC)
    def test_multiple_nodes(self):
        nodes = [TextNode("TEST 1: This is text with a `code block` word", TextType.TEXT),
         TextNode("TEST 2: This is text with a `code block` word", TextType.TEXT),
         TextNode("TEST 3: This is text with a `code block` word", TextType.TEXT),
         TextNode("##TEST B##", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes=nodes, delimiter="`", text_type=TextType.CODE)
        self.assertEqual(len(result), 10)
    def test_bold(self):
        nodes = [TextNode("TEST 1: This is text with a **code block** word", TextType.TEXT),
         TextNode("TEST 2: This is text with a `code block` word", TextType.TEXT),
         TextNode("TEST 3: This is text with a `code block` word", TextType.TEXT),
         TextNode("##TEST B##", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes=nodes, delimiter="**", text_type=TextType.BOLD)
        result = split_nodes_delimiter(old_nodes=result, delimiter="`", text_type=TextType.CODE)
        self.assertEqual(len(result), 10)
    
class Test_extract_links_and_imgs(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](link.com)"
        )
        self.assertListEqual([("link", "link.com")], matches)
    def test_alt_text_eq(self):
        img_text = "This is text with a link ![to boot dev](https://www.boot.dev)\
              \and ![to youtube](https://www.youtube.com/@bootdotdev)"
        link_text = "This is text with a link [to boot dev](https://www.boot.dev)\
              \and [to youtube](https://www.youtube.com/@bootdotdev)"
        img_matches = extract_markdown_images(img_text)
        link_matches = extract_markdown_links(link_text)
        self.assertEqual(img_matches, link_matches)
    def test_format_failure_eq(self):
        # Ensure that the functions don't pickup each-other's text.
        # Looks for empty lists.
        img_text = "This is text with a link ![to boot dev](https://www.boot.dev)\
              \and ![to youtube](https://www.youtube.com/@bootdotdev)"
        link_text = "This is text with a link [to boot dev](https://www.boot.dev)\
              \and [to youtube](https://www.youtube.com/@bootdotdev)"
        img_matches = extract_markdown_images(link_text) # img retriever looking for links
        link_matches = extract_markdown_links(img_text) # link retriever looking for images
        self.assertEqual(img_matches, link_matches)
    def test_links_not_images(self):
        img_text = "This is text with a link ![to boot dev](https://www.boot.dev)\
              \and ![to youtube](https://www.youtube.com/@bootdotdev)"
        img_matches = extract_markdown_images(img_text) 
        link_matches = extract_markdown_links(img_text) 
        self.assertNotEqual(img_matches, link_matches)
    
class Test_split_nodes_images_links(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images_links([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )
    def test_split_images_list(self):
        example_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        ]
        new_nodes = split_nodes_images_links(example_nodes)
        self.assertIsInstance(new_nodes, list)
    def test_find_images(self):
        example_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        ]
        img_iter = 0
        link_iter = 0
        new_nodes = split_nodes_images_links(example_nodes)
        for node in new_nodes:
            if node.text_type == TextType.IMAGE:
                img_iter += 1
            elif node.text_type == TextType.LINK:
                link_iter += 1
        self.assertGreater(link_iter, img_iter)
    def test_length_eq(self):
        example_node = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,)]
        new_nodes = split_nodes_images_links(example_node)
        self.assertEqual(len(new_nodes), 4)
    def test_url_exists(self):
        example_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,),
        TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        ]
        new_nodes = split_nodes_images_links(example_nodes)
        url_iter = 0
        for node in new_nodes:
            if node.url is not None:
                url_iter += 1
        # len(example_nodes) * 2 refers to the fact that each node in example_nodes has two urls
        self.assertEqual(url_iter, len(example_nodes)*2)

class Test_text_to_textnodes(unittest.TestCase):
    def test_all_delims_work(self):
        text_for_node = "This is **text** with an _italic_ word \
            and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev)"
        result = text_to_textnodes(text_for_node)
        self.assertEqual(len(result), 10)
    def test_all_delims_img_first(self):
        text_for_node = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev) This is **text** with an _italic_ word \
            and a `code block` and an"
        result = text_to_textnodes(text_for_node)
        self.assertEqual(len(result), 10)
    def test_all_delims_link_first(self):
        text_for_node = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev) This is **text** with an _italic_ word \
            and a `code block` and an"
        result = text_to_textnodes(text_for_node)
        self.assertEqual(len(result), 10)
    def test_all_delims_italics_first(self):
        text_for_node = "This an _italic_ word is **text** with  \
            and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev)"
        result = text_to_textnodes(text_for_node)
        self.assertEqual(len(result), 10)
    def test_class_is_textnode(self):
        text_for_node = "This an _italic_ word is **text** with  \
            and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev)"
        result = text_to_textnodes(text_for_node)
        self.assertIsInstance(result[1], TextNode)
    def test_class_is_list(self):
        text_for_node = "This an _italic_ word is **text** with  \
            and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev)"
        result = text_to_textnodes(text_for_node)
        self.assertIsInstance(result, list)
    def test_class_is_textnode(self):
        text_for_node = "This an _italic_ word is **text** with  \
            and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
                a [link](https://boot.dev)"
        result = text_to_textnodes(text_for_node)
        self.assertIsInstance(result[1], TextNode)
    



if __name__ == "__main__":
    unittest.main()
