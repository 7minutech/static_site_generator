from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"   
    CODE = "code"
    LINK = "link"
    IMG = "img"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, node):
        if self.text == node.text and self.text_type.value == node.text_type.value and self.url == node.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    text = text_node.text.replace("\n", " ")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img", "", {"src": text_node.url, "alt": text})
        case _:
            raise ValueError("All text nodes must have a text type")