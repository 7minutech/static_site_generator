import unittest
from block_markdown import *

class Test_MarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = (
"""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        )
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks, 
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_all_inlines(self):
        md = (
"""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
This is a paragarph with an anchor [boot dev](http//www.boot.dev.com)

This is a seperate paragraph with an img ![dog running](http//www.dog_running.png)

This is a _footer_ 
"""
        )
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks, 
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n"
                "This is a paragarph with an anchor [boot dev](http//www.boot.dev.com)",
                "This is a seperate paragraph with an img ![dog running](http//www.dog_running.png)",
                "This is a _footer_",
            ],
        )
    
    def test_markdown_to_blocks_many_block_elements(self):
        md = (
"""
#Welcome our website!

This is **best** website there is in the world
[image of the word](http//www.world.png)

1. We are the best
2. Look at number 1
3. Look at number 2

- Many peopele doubt
- They are wrong

> "The best website _there_ is ever."

This is a _footer_ 
"""
        )
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks, 
            [
                "#Welcome our website!",
                "This is **best** website there is in the world\n[image of the word](http//www.world.png)",
                "1. We are the best\n2. Look at number 1\n3. Look at number 2",
                "- Many peopele doubt\n- They are wrong",
                "> \"The best website _there_ is ever.\"",
                "This is a _footer_",
            ],
        )

    def test_markdown_to_blocks_start_end_newline(self):
        md = (
"""

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        )
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks, 
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    # --- Tests for block_to_block_type with headings 1-6 ---

    def test_block_to_block_type_heading1(self):
        h1_block = "# H1"
        self.assertEqual(block_to_block_type(h1_block), BlockType.HEADING)
    
    def test_block_to_block_type_heading2(self):
        h2_block = "## H2"
        self.assertEqual(block_to_block_type(h2_block), BlockType.HEADING)

    def test_block_to_block_type_heading3(self):
        h3_block = "### H3"
        self.assertEqual(block_to_block_type(h3_block), BlockType.HEADING)

    def test_block_to_block_type_heading4(self):
        h4_block = "#### H4"
        self.assertEqual(block_to_block_type(h4_block), BlockType.HEADING)

    def test_block_to_block_type_heading5(self):
        h5_block = "##### H5"
        self.assertEqual(block_to_block_type(h5_block), BlockType.HEADING)

    def test_block_to_block_type_heading6(self):
        h6_block = "###### H6"
        self.assertEqual(block_to_block_type(h6_block), BlockType.HEADING) 

    # --- Tests for block_to_block_type for code ---       

    def test_block_to_block_type_code(self):
        code_block = "```Ths is some code```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE) 
    
    def test_block_to_block_type_code_mutli_line(self):
        code_block = "```python\ndef my_function():\n   print(\"Hello\")\n    return 42\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE) 
    
    def test_block_to_block_type_missing_end_code(self):
        code_block = "```Ths is some code"
        self.assertNotEqual(block_to_block_type(code_block), BlockType.CODE) 
    
    def test_block_to_block_type_missing_start_code(self):
        code_block = "Ths is some code```"
        self.assertNotEqual(block_to_block_type(code_block), BlockType.CODE) 
    
    # --- Tests for block_to_block_type for quotes --- 

    def test_block_to_block_type_qoute(self):
        code_block = "> Ths is a quote block"
        self.assertEqual(block_to_block_type(code_block), BlockType.QUOTE) 
    
    # --- Tests for block_to_block_type for ul --- 

    def test_block_to_block_type_ul(self):
        ul_block = "- bullet 1\n- bullet 2\n- bullet 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST) 
    
    # --- Tests for block_to_block_type for ol --- 

    def test_block_to_block_type_ol(self):
        ol_block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST) 
    
    # --- Tests for block_to_block_type for paragraph --- 

    def test_block_to_block_type_paragraph(self):
        paragraph_block = "This is normal text"
        self.assertEqual(block_to_block_type(paragraph_block), BlockType.PARAGRAPH) 
        

class TestmMrkdownToHtmlNode(unittest.TestCase):
    
    # --- Test for helper method block_to_tag ---

    def test_block_to_tag_headings(self):
        heading_blocks = ["# H1", "## H2","### H3","#### H4","##### H5","###### H6",] 
        tags = []
        for heading_block in heading_blocks:
            tags.append(block_to_tag(heading_block, block_to_block_type(heading_block)))
        self.assertListEqual(["h1","h2","h3","h4","h5","h6"], tags)
    
    def test_block_to_tag_paragraph(self):
        paragraph_block = "This is normal text"
        tag = block_to_tag(paragraph_block, block_to_block_type(paragraph_block))
        self.assertEqual("p", tag)
    
    def test_block_to_tag_code(self):
        paragraph_block = "```This is text is code```"
        tag = block_to_tag(paragraph_block, block_to_block_type(paragraph_block))
        self.assertEqual("code", tag)
    
    def test_block_to_tag_quote(self):
        paragraph_block = "> This is a quote"
        tag = block_to_tag(paragraph_block, block_to_block_type(paragraph_block))
        self.assertEqual("blockquote", tag)
    
    def test_block_to_tag_ul(self):
        paragraph_block = "- Bullet one\n- Bullet two\n- Bullet three"
        tag = block_to_tag(paragraph_block, block_to_block_type(paragraph_block))
        self.assertEqual("ul", tag)
    
    def test_block_to_tag_ol(self):
        paragraph_block = "1. Point one\n2. Point two\n3. Point three"
        tag = block_to_tag(paragraph_block, block_to_block_type(paragraph_block))
        self.assertEqual("ol", tag)
    
    # --- Test for helper method block_to_text_value ---

    def test_block_to_text_value_headings(self):
        heading_blocks = ["# H1", "## H2","### H3","#### H4","##### H5","###### H6",] 
        actual = []
        for heading in heading_blocks:
            actual.append(block_to_text_value(heading, block_to_block_type(heading)))
        self.assertListEqual(["H1","H2","H3","H4","H5","H6"], actual)
    
    def test_block_to_text_value_paragraph(self):
        block = "This is some paragraph with a newline\nAnd some more new lines"
        self.assertEqual("This is some paragraph with a newline And some more new lines", block_to_text_value(block, block_to_block_type(block)))
    
    def test_block_to_text_value_code(self):
        block = "``` This is text that _should_ remain\nthe **same** even with inline stuff```"
        self.assertEqual("This is text that _should_ remain\nthe **same** even with inline stuff", block_to_text_value(block, block_to_block_type(block)))
    
    def test_block_to_text_value_quote(self):
        block = "> This is a quote with some _italic_ and **bold**"
        self.assertEqual("This is a quote with some _italic_ and **bold**", block_to_text_value(block, block_to_block_type(block)))
    
    # --- Test markdown_to_html_node ---

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
# Heading 1

This is **bolded** paragraph
text in a p
tag here

## Heading 2

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><h2>Heading 2</h2>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_ul(self):
        md = """

- This is **bolded** bullet
- This is _italic_ bullet
- This is `code` bullet

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> bullet</li><li>This is <i>italic</i> bullet</li><li>This is <code>code</code> bullet</li></ul></div>"
        )

    def test_ol(self):
        md = """

1. This is **bolded** first bullet
2. This is _italic_ second bullet
3. This is `code` third bullet

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> first bullet</li><li>This is <i>italic</i> second bullet</li>"
            "<li>This is <code>code</code> third bullet</li></ol></div>"
        )