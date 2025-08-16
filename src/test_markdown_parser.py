import unittest

from markdown_parser import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    # --- Tests for split_nodes_delimiter CODE, BOLD, and ITALIC ---
    
    def test_delimiter_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_delimiter_with_bold(self):
        node = TextNode("This is text with a **bold word** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_delimiter_with_italic_underscore(self):
        node = TextNode("This is text with a _italic word_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_delimiter_with_italic_star(self):
        node = TextNode("This is text with a *italic word* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ])
    
    # --- Tests for split_nodes_delimiter nested and w/ and w/o hits ---
    
    def test_delimiter_ignore_nested(self):
        node = TextNode("This is an _italic and **bold** word_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic and **bold** word", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
            ])
    
    def test_delimiter_no_hit(self):
        node = TextNode("This is a normal word word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a normal word word.", TextType.TEXT),
            ])
    
    def test_delimiter_many_hits(self):
        node = TextNode("This is **text** with a **bold word** word and that is **it**!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" word and that is ", TextType.TEXT),
            TextNode("it", TextType.BOLD),
            TextNode("!", TextType.TEXT),
            ])
    
    # --- Tests for split_nodes_delimiter non TEXT type ---
    
    def test_delimiter_non_text_type(self):
        node = TextNode("1984", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("1984", TextType.ITALIC),
            ]
    )
    
    # --- Tests for split_nodes_delimiter many nodes passed ---

    def test_delimiter_with_many_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with another `code block` word", TextType.TEXT)
        node3 = TextNode("bold word", TextType.BOLD)
        node4 = TextNode("This is text with without a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3, node4], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode("This is text with without a code block word", TextType.TEXT),
            ])


if __name__ == "__main__":
    unittest.main()