from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unorederd_list"
    ORDERED_LIST = "ordered_list"\
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    return blocks

def block_to_block_type(block):
    first_char = block[0]
    split_blocks = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
            
    if split_blocks[0].startswith("```") and split_blocks[-1].endswith("```"):
        return BlockType.CODE

    is_quote = True
    is_ul = True
    is_ol = True
    counter = 1
    for split_block in split_blocks:
        if split_block[0] != ">":
            is_quote = False
        if split_block[0:2] != "- ":
            is_ul = False
        if not split_block.startswith(f"{counter}. "):
            is_ol = False
        else:
            counter += 1
        if not is_quote and not is_ul and not is_ol:
            return BlockType.PARAGRAPH
    
    if is_quote:
        return BlockType.QUOTE
    if is_ul:
        return BlockType.UNORDERED_LIST
    if is_ol:
        return BlockType.ORDERED_LIST

