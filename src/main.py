from textnode import TextNode, TextType
import os, shutil

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    copy_to_destination("static", "public")

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


main()