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
    # headings
    match = re.search(r"(^\#{1,6})( )(.+)", markdown)
    if match:
        return BlockType.HEADING
    # multi-line code blocks
    match = re.search(r"(^```\n)(.*?)(\n```$)", markdown)
    if match:
        return BlockType.CODE
    # quote block
    markdown_lines = markdown.splitlines()
    is_quote = all(re.search(r"^>", line) for line in markdown_lines)
    if is_quote:
        return BlockType.QUOTE
    # unordered list
    is_unordered_list = all(re.search(r"(^-\s)", line) for line in markdown_lines)
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    # ordered list
    is_ordered_list = all(re.search(r"(^\d+\.\s)", line) for line in markdown_lines)
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    # default case: paragraph
    return BlockType.PARAGRAPH
