from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []

    for i in range(0, len(old_nodes)):
        
        if old_nodes[i].text_type != TextType.TEXT:
            list_of_nodes.append(old_nodes[i])
        else:
            inner_list = old_nodes[i].text.split(delimiter)
            if len(inner_list) % 2 == 0:
                raise Exception("invalid markdown")

            for i in range(0, len(inner_list)):  
                if (i) % 2 == 0: 
                    list_of_nodes.append(TextNode(inner_list[i], TextType.TEXT))
                else:
                    list_of_nodes.append(TextNode(inner_list[i], text_type))

    return list_of_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[.*?\]\(\S*\)", text)
    alt_text = []
    urls = []
    for item in matches:
        alt_text.append(re.findall(r"(?<=!\[).*(?=\])", item)[0])
        urls.append(re.findall(r"(?<=\().*?(?=\))", item)[0])
        # print("EXTRACT_MD_IMGS_DB")
    return list(zip(alt_text, urls))        

link_sample = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[[^\]]*]\(\S*\)", text)
    alt_text = []
    urls = []
    for item in matches:
        alt_text.append(re.findall(r"(?<=\[).*(?=\])", item)[0])
        urls.append(re.findall(r"(?<=\().*?(?=\))", item)[0])
    return list(zip(alt_text, urls))        

#### Split_nodes Function is below helper functions!! ####
    
example_node = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,)]

example_text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# example_text = '''This is text with a link ![to boot dev](https://www.boot.dev) 
# and [to youtube](https://www.youtube.com/@bootdotdev)'''


# example_text = md = '''1. This is a random first-line!
#         2. It's also got some funky-fresh(!!!) code blocks in it.
#         3. Look it says moranium!
#         4. And I think that's pretty friggin' cool!

#         5. Blah blach blah
#         6. Random text here!
#         '''

# Text extractor breaks the strings up into their component parts
def text_extractor(text):
    remaining_text = text
    result = []

    while remaining_text:
        # extract image if image is at start of string
        match = re.match(r"^!\[.*?\]\(.*?\)", remaining_text) 
        if match:
            result.append(match.group())
            remaining_text = remaining_text[match.end():] # removes matched string from string
            continue
        # extract link if link is at start of string
        match = re.match(r"^\[.*?\]\(.*?\)", remaining_text)
        if match:
            result.append(match.group())
            remaining_text = remaining_text[match.end():] # removes matched string from string
            continue

        # Matches plain text at start of string 
        match = re.match(r"^[^\[]+?(?=(?:!?\[)|$)", remaining_text) 
        if match:
            matched_text = match.group()
            if matched_text.strip() or '\n' in matched_text:
                result.append(matched_text)
            remaining_text = remaining_text[match.end():] # removes matched string from string
        else:
            # If no more matches
            # result.append(remaining_text)
            if remaining_text:
                result.append(remaining_text[0])
                remaining_text = remaining_text[1:]
            break

    return result

extractor_result = text_extractor(example_text)
# print(result)

# TextNode_formatter turns the images and links into tuples using the
# extract_markdown_images and extract_markdown_links functions and then 
# formats them into a proper list of text nodes
def TextNode_formatter(list):
    working_list = list.copy()
    for i in range(0, len(working_list)):
        # checks if image
        if working_list[i][0] == "!":
            # Creat tuple
            working_list[i] = extract_markdown_images(working_list[i])[0]
            # Turn to node
            working_list[i] = TextNode(working_list[i][0], TextType.IMAGE, working_list[i][1])
        # checks if link
        elif working_list[i][0] == "[":
            working_list[i] = extract_markdown_links(working_list[i])[0]
            # print(working_list[i])
            working_list[i] = TextNode(working_list[i][0], TextType.LINK, working_list[i][1])
        else:
            working_list[i] = TextNode(working_list[i], TextType.TEXT)
    
    return working_list

# result = TextNode_formatter(extractor_result)
# print(result)

def split_nodes_images_links(old_nodes):
    list_of_nodes = []
    
    for node in old_nodes:
        text = node.text
        text_list = text_extractor(text)
        list_processed = TextNode_formatter(text_list)
        list_of_nodes.append(list_processed)

    # flattens the list of lists into a single list
    result_list = [item for sublist in list_of_nodes for item in sublist]

    return result_list

# print(split_nodes_images_links([TextNode(example_text, TextType.TEXT)]))

### Overall Inline Function below ###

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    text_nodes = split_nodes_images_links(nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "__", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)

    # trialling to prevent parsing errors if node text is empty
    filtered_nodes = [node for node in text_nodes if not (node.text == "" and node.text_type == TextType.TEXT)]

    return filtered_nodes

# text_for_node = "This is **text** with an _italic_ word \
#             and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and \
#                 a [link](https://boot.dev)"

# result = text_to_textnodes(text_for_node)
# print(result)
