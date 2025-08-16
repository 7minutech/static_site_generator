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

def extract_markdown_images(text):
    matches = []
    alt_texts = re.findall(r"\[(.*?)\]", text)
    srcs = re.findall(r"\((.*?)\)", text)
    if len(alt_texts) != len(srcs):
        raise ValueError("Invalid markdown")
    for i in range(len(alt_texts)):
        matches.append((alt_texts[i], srcs[i]))
    return matches

def extract_markdown_links(text):
    matches = []
    anchor_texts = re.findall(r"\[(.*?)\]", text)
    hrefs = re.findall(r"\((.*?)\)", text)
    if len(anchor_texts) != len(hrefs):
        raise ValueError("Invalid markdown")
    for i in range(len(anchor_texts)):
        matches.append((anchor_texts[i], hrefs[i]))
    return matches