from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title
import os, shutil, sys

def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    print(basepath)
    copy_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_to_destination(source_path, destination_path):
    if os.path.isdir(source_path) and os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
        copy_dir_contents(source_path, destination_path)
    else:
        raise ValueError("source and destination must both be dirs")

def copy_dir_contents(dir_path, destination):
    dir_contents = os.listdir(dir_path)
    for item in dir_contents:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            new_dir_path = os.path.join(destination, item)
            os.mkdir(new_dir_path)
            copy_dir_contents(item_path, new_dir_path)
        else:
            print(f"copying {item_path} to {destination}")
            shutil.copy(item_path, destination)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        markdown_contents = ""
        template_contents = ""
        with open(from_path) as markdown:
            markdown_contents = markdown.read()
        with open(template_path) as html_template:
            template_contents = html_template.read()
        html_str = markdown_to_html_node(markdown_contents).to_html()
        title_of_page = extract_title(markdown_contents)
        template_contents = template_contents.replace("{{ Title }}", title_of_page)
        template_contents = template_contents.replace("{{ Content }}", html_str)
        template_contents = template_contents.replace("href=\"/", f"href=\"{basepath}")
        template_contents = template_contents.replace("src=\"/", f"src=\"{basepath}")
        if not os.path.exists(os.path.join(os.getcwd(), os.path.dirname(dest_path))):
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(dest_path)))
        with open(dest_path, "w") as html_file:
            html_file.write(template_contents)
            
    except FileNotFoundError as fe:
        print(f"file: {from_path} was not found: {fe}")
    except Exception as e:
        print(f"error occured: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    source_dir_contents = os.listdir(dir_path_content)
    for item in source_dir_contents:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            new_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dir_path, basepath)
        else:
            md_file_path = os.path.join(dest_dir_path, item)
            html_file_path = os.path.splitext(md_file_path)[0] + ".html"
            generate_page(item_path, template_path, html_file_path, basepath)



main()