import unittest

from htmlnode import HTMLNode


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
    


if __name__ == "__main__":
    unittest.main()