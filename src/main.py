from textnode import TextNode
from htmlnode import HTMLNode
from site_copier import static_site_copier, generate_page, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    
    # Example stuff
    # text_node = TextNode("placeholder text", "link", "https://www.website.com") # placeholder values
    # html_node = HTMLNode("h1", "a headline", ["placeholder", "children"], {
    #                     "href": "https://www.google.com", "target": "_blank", }) # placeholder values
    # print(text_node) # uses __repr__
    # print(html_node)  # uses __repr__
    
    # Deletes the public directory and copies files from static to public
    static_site_copier()

    # DEPRECATED for the "Generates all" code below --- Generates a page from content/index.md using template.html and writes to public/index.html --- 
    # dest_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/public/index.html"
    # markdown_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/content/index.md"
    # template_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/template.html"
    # generate_page(markdown_path, template_path, dest_path)

    # Generates all files in content/ 
    content_p = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/content/"
    template_p = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/template.html"
    dest_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/docs/"
    generate_pages_recursive(content_p, template_p, dest_path, base_path)
    



if __name__ == "__main__": #ensures that function is only called if script is executed directly
    main()