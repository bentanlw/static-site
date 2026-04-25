import unittest

from textnode import TextType, TextNode

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


if __name__=="__main__":
    unittest.main()
