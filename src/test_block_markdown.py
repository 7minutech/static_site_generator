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