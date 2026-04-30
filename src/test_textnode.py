import unittest

from textnode import TextType, TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_texttype_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_noteq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("link", TextType.LINK, "http://www.boot.dev")
        node2 = TextNode("link", TextType.LINK, "http://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_default_none(self):
        node = TextNode("text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_all_text_types_distinct(self):
        types = list(TextType)
        nodes = [TextNode("x", t) for t in types]
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                if i == j:
                    self.assertEqual(n1, n2)
                else:
                    self.assertNotEqual(n1, n2)

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD, "http://example.com")
        self.assertEqual(repr(node), "TextNode(Hello, bold, http://example.com)")

    def test_repr_no_url(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(Hello, text, None)")

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

if __name__=="__main__":
    unittest.main()
