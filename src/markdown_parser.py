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
        else:
            imgs = extract_markdown_images(node.text)
            parsed_text = node.text.split("!")
            imgs_count = len(imgs)
            hits = 0
            for text in parsed_text:
                alt_text = imgs[hits][0]
                url = imgs[hits][1]
                img_text = f"[{alt_text}]" + f"({url})"
                
                if text.startswith(img_text) and hits < imgs_count:
                    new_nodes.append(TextNode(alt_text, TextType.IMG, url))
                    if text != img_text:
                        new_nodes.append(TextNode(text[len(img_text):], TextType.TEXT))
                    hits += 1
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            parsed_text = node.text.split("[")
            links_count = len(links)
            hits = 0
            for text in parsed_text:
                anchor_text = links[hits][0]
                url = links[hits][1]
                link_text = f"{anchor_text}]" + f"({url})"
                
                if text.startswith(link_text) and hits < links_count:
                    new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                    if text != link_text:
                        new_nodes.append(TextNode(text[len(link_text):], TextType.TEXT))
                    hits += 1
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)