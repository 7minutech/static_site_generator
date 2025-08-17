import unittest

from inline_markdown_parser import *
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
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
    
    def test_delimiter_empty_list(self):
        new_nodes = split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [])
    
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
    
    # --- Tests for split_nodes_delimiter invalid markdown ---

    def test_delimiter_invalid_markdown(self):
        node = TextNode("This text is _italic", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_images_many(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, extract_markdown_images(text))
    
    def test_extract_markdown_images_one(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_markdown_links_many(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, extract_markdown_links(text))
    
    def test_extract_markdown_links_one(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(expected, extract_markdown_links(text))

class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_image_between_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in between text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in between text.", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_image_with_link(self):
        node = TextNode(
            "![a](url1) text [my link](url2) ![b](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("a", TextType.IMG, "url1"),
            TextNode(" text [my link](url2) ", TextType.TEXT),
            TextNode("b", TextType.IMG, "url3"),
        ],
        new_nodes,
        )  
    
    def test_split_image_no_hits(self):
        node = TextNode(
            "This is normal text with no imgs",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is normal text with no imgs", TextType.TEXT),
        ],
        new_nodes,
        ) 
    
    def test_split_image_begin_and_end_with_imgs(self):
        node = TextNode(
            "![img1](url1)text![img2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("img1", TextType.IMG, "url1"),
            TextNode("text", TextType.TEXT),
            TextNode("img2", TextType.IMG, "url2")
        ],
        new_nodes,
        )  
    
    def test_split_image_adjacent_images(self):
        node = TextNode(
            "![img1](url1)![img2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("img1", TextType.IMG, "url1"),
            TextNode("img2", TextType.IMG, "url2")
        ],
        new_nodes,
        )  
    
    def test_split_image_invalid_markdown(self):
        node = TextNode(
            "![img[alt]](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("![img[alt]](url)", TextType.TEXT),
        ],
        new_nodes,
        )  
        
class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ],
        new_nodes,
        )  
    
    def test_split_image_between_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) in between text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in between text.", TextType.TEXT)
        ],
        new_nodes,
        ) 
    
    def test_split_link_with_img(self):
        node = TextNode(
            "![a](url1) text [my link](url2) ![b](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("![a](url1) text ", TextType.TEXT),
            TextNode("my link", TextType.LINK, "url2"),
            TextNode(" ![b](url3)", TextType.TEXT),
        ],
        new_nodes,
        )  
    
    def test_split_links_no_hits(self):
        node = TextNode(
            "This is normal text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is normal text with no links", TextType.TEXT),
        ],
        new_nodes,
        )  
    
    def test_split_link_begin_and_end_with_links(self):
        node = TextNode(
            "[link1](url1)text[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("text", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ],
        new_nodes,
        )  
    
    def test_split_link_adjacent_links(self):
        node = TextNode(
            "[link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2")
        ],
        new_nodes,
        )  
    
    def test_split_link_invalid_markdown(self):
        node = TextNode(
            "[link1[link2]](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("[link1[link2]](url)", TextType.TEXT),
        ],
        new_nodes,
        )  

class TestTextToTextnodes(unittest.TestCase):
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and" \
        " an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)
    
    def test_text_to_textnodes_with_both_italics(self):
        text = "This is **text** with an _italic_ word and a `code block` and" \
        " another *italic word* ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()