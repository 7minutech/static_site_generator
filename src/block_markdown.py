from enum import Enum
from htmlnode import *
from inline_markdown_parser import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unorederd_list"
    ORDERED_LIST = "ordered_list"
    
def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    return blocks

def block_to_block_type(block):
    split_blocks = block.strip().split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
            
    if split_blocks[0].startswith("```") and split_blocks[-1].endswith("```"):
        return BlockType.CODE

    is_quote = True
    is_ul = True
    is_ol = True
    counter = 1
    for split_block in split_blocks:
        if split_block[0] != ">":
            is_quote = False
        if split_block[0:2] != "- ":
            is_ul = False
        if not split_block.startswith(f"{counter}. "):
            is_ol = False
        else:
            counter += 1
        if not is_quote and not is_ul and not is_ol:
            return BlockType.PARAGRAPH
    
    if is_quote:
        return BlockType.QUOTE
    if is_ul:
        return BlockType.UNORDERED_LIST
    if is_ol:
        return BlockType.ORDERED_LIST

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_to_tag(block, block_type)
        html_node = HTMLNode(tag)
        text_nodes = text_to_textnodes(block)
        


def block_to_tag(block, block_type):
    match block_type:
        case BlockType.HEADING:
            level = (block.split(" "))[0].count("#")
            return f"h{level}"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        

# md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """

# node = markdown_to_html_node(md)
# html = node.to_html()
# print(html)
