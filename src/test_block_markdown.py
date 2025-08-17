import unittest
from block_markdown import markdown_to_blocks

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
