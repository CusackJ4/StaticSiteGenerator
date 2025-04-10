from textnode import TextNode
from htmlnode import HTMLNode

def main():
    text_node = TextNode("placeholder text", "link", "https://www.website.com") # placeholder values
    html_node = HTMLNode("h1", "a headline", ["placeholder", "children"], {
                        "href": "https://www.google.com", "target": "_blank", }) # placeholder values
    print(text_node) # uses __repr__
    print(html_node)  # uses __repr__

if __name__ == "__main__": #ensures that function is only called if script is executed directly
    main()