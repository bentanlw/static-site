import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    # split block into lines
    block_lines = markdown.split("\n")
    # heading should start with the 1-6 # followed by a space
    if re.search(r"(^#{1,6})( )(.+)", markdown):
        return BlockType.HEADING
    # code block should have more than one line, and start and end with ```
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        return BlockType.CODE
    # quote block should have > at start of every line
    if markdown.startswith(">"):
        for line in block_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # unordered list should start with - at every line, followed by a space
    if markdown.startswith("- "):
        for line in block_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    # ordered list has to have sequential numbering and a period after the number, and a space after that
    if markdown.startswith("1. "):
        i = 1
        for line in block_lines:
            if not line.startswith(f"{i}. "):
                   return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    # if none of the above fit, then paragraph
    return BlockType.PARAGRAPH
