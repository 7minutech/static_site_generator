import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    # --- Tests for props_to_html() ---
    
    def test_props_to_html(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=test_props)
        output = node.props_to_html()
        self.assertEqual(output, " href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        output = node.props_to_html()
        self.assertEqual(output, "")

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        output = node.props_to_html()
        self.assertEqual(output, "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "container"})
        output = node.props_to_html()
        self.assertEqual(output, ' class="container"')
    
    # --- Tests for LeafNode to_html() ---
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Here is some text.", props={"class": "text", "id": "first_quote"})
        self.assertEqual(node.to_html(), "<span class=\"text\" id=\"first_quote\">Here is some text.</span>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Here is some text with no tag.")
        self.assertEqual(node.to_html(), "Here is some text with no tag.")

if __name__ == "__main__":
    unittest.main()