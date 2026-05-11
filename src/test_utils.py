import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_image, split_nodes_link, text_node_to_html_node, split_nodes_delimiter, text_to_textnodes

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("click me", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click me")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/cat.png", "alt": "a cat"})

    def test_invalid_type_raises(self):
        node = TextNode("text", TextType.TEXT)
        node.text_type = "not_a_type"
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_node_passed_through(self):
        # non-TEXT nodes should be left alone
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_no_delimiter_in_text(self):
        # no delimiter present — node returned unchanged
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("plain text", TextType.TEXT)])

    def test_multiple_nodes(self):
        # mix of node types in the input list
        nodes = [
            TextNode("Hello `code` world", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ])
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "![cat](https://example.com/cat.png) and ![dog](https://example.com/dog.png)"
        )
        self.assertListEqual([
            ("cat", "https://example.com/cat.png"),
            ("dog", "https://example.com/dog.png"),
        ], matches)

    def test_no_images(self):
        matches = extract_markdown_images("just plain text")
        self.assertListEqual([], matches)

    def test_ignores_plain_links(self):
        # links without ! should not be returned
        matches = extract_markdown_images("[not an image](https://example.com)")
        self.assertListEqual([], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        matches = extract_markdown_links("Here is a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "[one](https://one.com) and [two](https://two.com)"
        )
        self.assertListEqual([
            ("one", "https://one.com"),
            ("two", "https://two.com"),
        ], matches)

    def test_no_links(self):
        matches = extract_markdown_links("just plain text")
        self.assertListEqual([], matches)

    def test_ignores_images(self):
        # image syntax should not be returned
        matches = extract_markdown_links("![image](https://example.com/img.png)")
        self.assertListEqual([], matches)

    def test_mixed_images_and_links(self):
        matches = extract_markdown_links(
            "![img](https://example.com/img.png) and [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode("This is text with a [link](https://boot.dev) and more", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and more", TextType.TEXT),
        ], new_nodes)

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://example.com"),
        ], new_nodes)

    def test_no_links_unchanged(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], new_nodes)

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

    def test_ignores_images(self):
        node = TextNode("![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("![image](https://example.com/img.png)", TextType.TEXT)], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_multi_formats(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_nodes)

    def test_plain_text(self):
        new_nodes = text_to_textnodes("just plain text")
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], new_nodes)

    def test_bold_only(self):
        new_nodes = text_to_textnodes("**bold**")
        self.assertListEqual([TextNode("bold", TextType.BOLD)], new_nodes)

    def test_italic_only(self):
        new_nodes = text_to_textnodes("_italic_")
        self.assertListEqual([TextNode("italic", TextType.ITALIC)], new_nodes)

    def test_code_only(self):
        new_nodes = text_to_textnodes("`code`")
        self.assertListEqual([TextNode("code", TextType.CODE)], new_nodes)

    def test_image_only(self):
        new_nodes = text_to_textnodes("![alt](https://example.com/img.png)")
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
        ], new_nodes)

    def test_link_only(self):
        new_nodes = text_to_textnodes("[click](https://boot.dev)")
        self.assertListEqual([
            TextNode("click", TextType.LINK, "https://boot.dev"),
        ], new_nodes)

    def test_image_and_link(self):
        new_nodes = text_to_textnodes("![img](https://example.com/img.png) and [link](https://boot.dev)")
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_single_block(self):
        blocks = markdown_to_blocks("just one paragraph")
        self.assertEqual(blocks, ["just one paragraph"])

    def test_strips_leading_trailing_whitespace(self):
        blocks = markdown_to_blocks("  leading spaces  \n\n  trailing spaces  ")
        self.assertEqual(blocks, ["leading spaces", "trailing spaces"])

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_only_newlines(self):
        blocks = markdown_to_blocks("\n\n\n\n")
        self.assertEqual(blocks, [])

    def test_multiple_blank_lines_between_blocks(self):
        blocks = markdown_to_blocks("block one\n\n\n\nblock two")
        self.assertEqual(blocks, ["block one", "block two"])

    def test_preserves_internal_newlines(self):
        blocks = markdown_to_blocks("line one\nline two\n\nline three")
        self.assertEqual(blocks, ["line one\nline two", "line three"])


if __name__ == "__main__":
    unittest.main()
