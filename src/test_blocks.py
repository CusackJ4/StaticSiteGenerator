import unittest
from block_functions import *

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_empty_space(self):
        md = '''# This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.



        - This is the first list item in a list block
        - This is a list item
        - This is another list item'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["# This is a heading",
                          "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                          "- This is the first list item in a list block\n- This is a list item\n- This is another list item"]
                         )
    def test_markdown_to_blocks_again(self):
        md = """



        # Hello!
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Hello!"])

class Test_block_to_block_type(unittest.TestCase):
    def test_heading_eq(self):
        ex_block = "#### This is a dope-ass heading!"
        ex_block2 = "# This is a dope-ass heading!"
        ex_block3 = "##This is a dope-ass heading!" # deliberately wrong to fail
        iter = 0
        for list in [ex_block, ex_block2, ex_block3]:
            result = block_to_block_type(list)
            if result == BlockType.HEADING:
                iter += 1
        self.assertEqual(iter, 2)
    def test_paragraph_eq(self):   
        ex_block = '''This is a dope-ass heading!
        It's also got some funky-fresh(!!!) code blocks in it. (No it doesn't.)
        Look it says moranium!
        And I think that's pretty friggin' cool!
        '''
        result = block_to_block_type(ex_block)
        self.assertEqual(result, BlockType.PARAGRAPH)     
    def test_code(self):
        ex_code = '''```Hellow World!!```
        '''
        result = block_to_block_type(ex_code)
        self.assertEqual(result, BlockType.CODE)
    def test_quote(self):
        ex_quote = '''>### This is a dope-ass heading!\
        >It's also got some funky-fresh(!!!) code blocks in it.\
        >Look it says I love moranium!!\
        >And I think that's pretty friggin' cool!
        '''
        result = block_to_block_type(ex_quote)
        self.assertEqual(result, BlockType.QUOTE)
    def test_unordered_list(self):
        ex_uList = '''- ### This is not a dope-ass heading!\
        - It's also got some funky-fresh(!!!) code blocks in it.\
        - Look it says moranium!!?\
        - And I think that's pretty friggin' cool!\
        '''
        result = block_to_block_type(ex_uList)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        ex_oList = '''1. ### This is a dope-ass heading!\
        2. It's also got some funky-fresh(!!!) code blocks in it.\
        3. Look it says moranium!\
        4. And I think that's pretty friggin' cool!\
        '''
        result = block_to_block_type(ex_oList)
        self.assertEqual(result, BlockType.ORDERED_LIST)
     
class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headers_lists_paragraphs(self):
        md = '''## First Header

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        ### second header!

        - This is the first list item in a list block
        - This is a list item
        - This is another list item'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>First Header</h2><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><h3>second header!</h3><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>",
        )
    def test_two_ordered_lists(self):
        md = '''1. This is a random first-line!
        2. It's also got some funky-fresh(!!!) code blocks in it.
        3. Look it says moranium!
        4. And I think that's pretty friggin' cool!

        5. Blah blach blah
        6. Random text here!
        '''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a random first-line!</li><li>It's also got some funky-fresh(!!!) code blocks in it.</li><li>Look it says moranium!</li><li>And I think that's pretty friggin' cool!</li></ol><ol><li>Blah blach blah</li><li>Random text here!</li></ol></div>",
        )
    def test_two_unordered_lists(self):
        md = '''- This is a random first-line!
        - It's also got some funky-fresh(!!!) code blocks in it.
        - Look it says moranium!
        - And I think that's pretty friggin' cool!

        - Blah blach blah
        - Random text here!
        '''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a random first-line!</li><li>It's also got some funky-fresh(!!!) code blocks in it.</li><li>Look it says moranium!</li><li>And I think that's pretty friggin' cool!</li></ul><ul><li>Blah blach blah</li><li>Random text here!</li></ul></div>",
        )
    def test_two_blockquotes(self):
        md = '''>### This is a dope-ass heading!
        >It's also got some funky-fresh(!!!) **bold content** in it.
        >Look it says I love moranium!!
        >And I think that's pretty friggin' cool!

        >another
        >blockquote!
        '''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '''<div><blockquote>### This is a dope-ass heading!
It's also got some funky-fresh(!!!) <b>bold content</b> in it.
Look it says I love moranium!!
And I think that's pretty friggin' cool!</blockquote><blockquote>another
blockquote!</blockquote></div>''',
        )
    def test_header(self):
        md = "## header and **bold** content"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>header and <b>bold</b> content</h2></div>",
        )
    






if __name__ == "__main__":
    unittest.main()