import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    # --- Tests for ParentNode to_html() ---

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_many_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("div", [grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><div><p>grandchild2</p></div></div>",
        )

    def test_to_html_with_many_children(self):
        child_node = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span><span>child3</span></div>")
    
    def test_to_html_with_deep_verticle_nesting(self):
        level_5 = LeafNode("p", "last level")
        level_4 = ParentNode("span", [level_5])
        level_3 = ParentNode("div", [level_4])
        level_2 = ParentNode("div", [level_3])
        level_1 = ParentNode("main", [level_2])
        parent_node = ParentNode("body", [level_1])
        self.assertEqual(parent_node.to_html(), "<body><main><div><div><span><p>last level</p></span></div></div></main></body>")
    
    def test_to_html_with_deep_wide_nesting(self):
        footer_div = LeafNode("div", "footer text")
        main_div = LeafNode("div", "main text")
        header_div = LeafNode("div", "header text")
        footer = ParentNode("footer", [footer_div])
        main = ParentNode("main", [main_div])
        header = ParentNode("header", [header_div])
        parent_node = ParentNode("body", [header, main, footer])
        self.assertEqual(parent_node.to_html(), ("<body>"
        "<header><div>header text</div></header>"
        "<main><div>main text</div></main>"
        "<footer><div>footer text</div></footer>"
        "</body>"))
    
    def test_to_html_with_many_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild1", props={"id": "first_grandchild"})
        grandchild_node2 = LeafNode("p", "grandchild2", props={"id": "second_grandchild"})
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("div", [grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node2], props={"class": "top_level"})
        self.assertEqual(
            parent_node.to_html(),
            ("<div class=\"top_level\"><span><b id=\"first_grandchild\">grandchild1</b></span>"
            "<div><p id=\"second_grandchild\">grandchild2</p></div></div>")
        )

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
if __name__ == "__main__":
    unittest.main()