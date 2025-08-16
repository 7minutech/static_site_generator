from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (node.text).count(delimiter) % 2 != 0:
            raise ValueError("text is not valid markdown")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parsed_text = (node.text).split(delimiter)
            for i in range(len(parsed_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(parsed_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parsed_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            imgs = extract_markdown_images(node.text)
            text = node.text
            
            for img in imgs:
                img_text = f"![{img[0]}]({img[1]})"
                parts = text.split(img_text, 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(img[0], TextType.IMG, img[1]))
                text = parts[-1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            text = node.text
            for link in links:
                link_text = f"[{link[0]}]({link[1]})"
                parts = text.split(link_text, 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                text = parts[-1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)