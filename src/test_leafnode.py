import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    # tag edge cases
    def test_no_tag_returns_raw_value(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_no_tag_no_props(self):
        # props are irrelevant without a tag
        node = LeafNode(None, "raw", {"class": "x"})
        self.assertEqual(node.to_html(), "raw")

    # value edge cases
    def test_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_string_value_raises(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    # props edge cases
    def test_no_props(self):
        node = LeafNode("b", "bold")
        self.assertEqual(node.to_html(), "<b>bold</b>")

    def test_multiple_props(self):
        node = LeafNode("a", "link", {"href": "https://example.com", "target": "_blank"})
        html = node.to_html()
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith("<a ") and html.endswith("</a>"))

    def test_empty_props_dict(self):
        node = LeafNode("p", "text", {})
        self.assertEqual(node.to_html(), "<p>text</p>")
   
