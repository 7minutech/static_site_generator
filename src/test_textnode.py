import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    # --- Tests for equal behavior ---
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    # --- Tests for not equal behavior ---

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node that is different", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node with different text", TextType.BOLD, "https://www.dev.boot")
        self.assertNotEqual(node, node2)
    
    # --- Tests for default property values ---

    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()