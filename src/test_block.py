import unittest

from block import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block_type = block_to_block_type("#### heading 4")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md ="```\nthis is a code block\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block_type = block_to_block_type(">this is a quote\n>like, multi\n>quote")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block_type = block_to_block_type("- this is a list\n- like, multi\n- unordered list")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block_type = block_to_block_type("1. this is a list\n2. like, multi\n3. ordered list")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block_type = block_to_block_type("just a plain paragraph")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # heading edge cases
    def test_heading_all_levels(self):
        for i in range(1, 7):
            block_type = block_to_block_type(f"{'#' * i} heading {i}")
            self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        # 7 # chars should NOT be a heading
        block_type = block_to_block_type("####### not a heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        block_type = block_to_block_type("#no space after hash")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # code edge cases
    def test_code_block_no_closing_fence_is_paragraph(self):
        block_type = block_to_block_type("```\nno closing fence")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # quote edge cases
    def test_quote_missing_marker_on_one_line_is_paragraph(self):
        # one line lacks >, so should not be a quote
        block_type = block_to_block_type(">valid quote\nnot a quote line\n>another")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # unordered list edge cases
    def test_unordered_list_missing_marker_is_paragraph(self):
        block_type = block_to_block_type("- item one\nitem two missing marker\n- item three")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # ordered list edge cases
    def test_ordered_list_multi_digit(self):
        items = "\n".join(f"{i}. item" for i in range(1, 12))
        block_type = block_to_block_type(items)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_missing_marker_is_paragraph(self):
        block_type = block_to_block_type("1. item one\nitem two missing\n3. item three")
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
