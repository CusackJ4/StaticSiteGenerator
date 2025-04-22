import shutil
import os
from contextlib import suppress
from block_functions import markdown_to_html_node

### Public-Static copying function
def copy_static_folder(current_path, target_path):
    # start by producing directory of contents
    src_path = current_path
    dst_path = target_path
    dir_list = os.listdir(path = src_path)


    # then copy all files
    for dir_item in dir_list:
        joined_path = os.path.join(src_path, dir_item)

        # Checks to see if path is to a file
        if os.path.isfile(joined_path):
            print("file created")

            # copies file to target path
            shutil.copy(joined_path, 
                dst_path)
            
    # then search in folders and recurse
    for dir_item in dir_list:

        # joined_path = path to subdirectory
        joined_path = os.path.join(src_path, dir_item)

        # checks to see if path is to a directory
        if os.path.isdir(joined_path):
            print("dir created")

            # create path for new directory in /public
            dst_path = os.path.join(dst_path, dir_item)
            os.makedirs(dst_path)
            
            # source path becomes path to subdirectory
            src_path = joined_path

            # recurse within subdirectory
            copy_static_folder(src_path, dst_path)
    
    return

def static_site_copier():
    static_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/static/"
    public_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/public/"

    # Delete public directory
    with suppress(FileNotFoundError):
        print("public folder deleted!")
        shutil.rmtree(public_path)
    # Make public directory
    os.makedirs(public_path)
    print("public folder created!")

    # Use function
    copy_static_folder(static_path, public_path)

    return


## Markdown Extractor
def extract_title(markdown, contents):
    split_lines = contents.split("\n")
    markdown = "# " if markdown == "#" else markdown

    for line in split_lines:
        if line.startswith(markdown):
            line = line.strip("#").strip()
            return line
    raise Exception("Target markdown not found!!")

# Function in-use:
# optional params -- all this could go straight into func signature hypothetically
path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/content/index.md"
target = "# Tolkien"
with open(path) as f:
        file_md = f.read()
result = extract_title("#", file_md)
# print(result)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_from_path = f.read()
    with open(template_path) as f:
        template_path_contents = f.read()    
    html_string = markdown_to_html_node(markdown_from_path).to_html()
    title = extract_title("#", markdown_from_path)
    print(title)
    template_contents = template_path_contents.replace("{{ Title }}", title)\
        .replace("{{ Content }}", html_string)
    with open(dest_path, "w") as f:
        f.write(template_contents)
    return template_contents

dest_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/public/index.html"
markdown_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/content/index.md"
template_path = "/Users/jeffshomefolder/codeworkspace/StaticSiteGenerator/template.html"

generate_page(markdown_path, template_path, dest_path)




