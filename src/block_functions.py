import re
from enum import Enum
from textnode import *
from htmlnode import *
from inline_functions import *


test_md = """
- Item 1
- Item 2
- Item 3
"""

def markdown_to_blocks(markdown):
    blocks = []
    trimmed = markdown.strip()
    # separates markdown into blocks based on '\n\n'
    for part in trimmed.split('\n\n'):
        # checks to see if anything is there by checking if part.strip() returns None
        if not part.strip():
            continue
        # separates lines into a list on '\n' and strips out excess whitespace
        lines = [line.strip() for line in part.split('\n')]
        # rejoins the lines together into a block, adding '\n' as the delim, and appends to 'blocks' list
        blocks.append('\n'.join(lines))

    return blocks



class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(markdown):
    var = re.findall(r"^#{1,6}\s{1}(?=.+)", markdown)
    if var:
        return BlockType.HEADING
    var = re.findall(r"^`{3}[\s\S]+?`{3}", markdown, re.MULTILINE)
    if var:
        return BlockType.CODE
    var = re.findall(r"^>", markdown, flags=re.MULTILINE)
    if len(var) == len(markdown.strip().split("\n")):
        return BlockType.QUOTE
    var = re.findall(r"^-{1}\s{1}", markdown, flags=re.MULTILINE)
    if len(var) == len(markdown.strip().split("\n")):
        return BlockType.UNORDERED_LIST
    var = re.findall(r"^\d+\.{1}\s{1}", markdown, flags=re.MULTILINE)
    if len(var) == len(markdown.strip().split("\n")):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# type_result = block_to_block_type(test_md)

# print(f"Block type detected: {type_result}")

def text_to_children(markdown):
    text_nodes = text_to_textnodes(markdown)
    
    children_nodes = []

    # returns correct tag and value per-node
    for node in text_nodes:
        
        leaf_node = text_node_to_html_node(node)
        children_nodes.append(leaf_node)
    
    return children_nodes



def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    
    parent_node = ParentNode("div", [])
    # for block in block_list:
    for i, block in enumerate(block_list):
        # print(f"Processing block {i}: {block[:30]}...")  # Print first 30 chars
    # Then your existing code
        block_type = block_to_block_type(block)
        # print(f"The Block Type is {block_type}")
        # print(f"About to process text: {block[:50]}...")
        
        match block_type:
            case BlockType.PARAGRAPH:
                # print("Processing paragraph")
                block_node = ParentNode(tag = "p", children = [], props={})
                block = block.replace("\n", " ")
                # print(f"About to process text: {block[:50]}...")
                child_nodes = text_to_children(block)
                # print(f"Got {len(child_nodes)} child nodes")
                # print(list(child_nodes))
                block_node.children = child_nodes
                parent_node.children.append(block_node)
            case BlockType.HEADING:
                h_length = len(re.match(r'#*', block).group())
                h_tag = "h" + str(h_length)
                block_node = ParentNode(tag = h_tag, children = [], props={})
                block = block.replace("\n", " ")
                block = re.sub("^#*\s", "", block, flags=re.MULTILINE)
                child_nodes = text_to_children(block)
                block_node.children = child_nodes
                parent_node.children.append(block_node)
            case BlockType.CODE:
                block_node = ParentNode(tag = "pre", children = [], props={})
                block = block.replace("```", "")
                if block.startswith("\n"):
                    block = block[1:]
                text_node = TextNode(block, TextType.CODE)
                child_node = text_node_to_html_node(text_node)
                block_node.children = [child_node]
                parent_node.children.append(block_node)
            case BlockType.QUOTE:
                block_node = ParentNode(tag = "blockquote", children = [], props={})
                
                
                # block = block.replace(">", "")
                block = block.replace(">", "").strip()
                lines = block.split("\n")
                processed_text = " ".join([line.strip() for line in lines if line.strip()])
                child_nodes = text_to_children(processed_text)

                # child_nodes = text_to_children(block)
                block_node.children = child_nodes
                parent_node.children.append(block_node)
                
            case BlockType.UNORDERED_LIST:
                block_node = ParentNode(tag = "ul", children = [], props={})
                
                lines = block.split("\n")
                child_nodes = []
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith(("- ", "* ", "+ ")):
                        line_text = line[2:]
                        # Create a list item node
                        li_node = ParentNode(tag="li", children=text_to_children(line_text), props={})
                        # Add the list item to the unordered list
                        block_node.children.append(li_node)

                parent_node.children.append(block_node)
                
            case BlockType.ORDERED_LIST:
                block_node = ParentNode(tag = "ol", children = [], props={})
                
                lines = block.split("\n")
                child_nodes = []
                for line in lines:
                    if not line.strip():
                        continue
                    stripped = line.strip()
                    line_text = re.sub(r'^\d+\.\s+', '', stripped)
                    # Create a list item node
                    li_node = ParentNode(tag="li", children=text_to_children(line_text), props={})
                    # Add the list item directly to the ordered list
                    block_node.children.append(li_node)
    
                parent_node.children.append(block_node)

    return parent_node



