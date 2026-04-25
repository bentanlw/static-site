import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
                "div",
                "Hello, world!",
                None,
                {"class": "greeting", "href": "https://boot.dev"},
                )
        self.assertEqual(
                node.props_to_html(),
                ' class="greeting" href="https://boot.dev"',
                )

    def test_values(self):
        node = HTMLNode(
                "div",
                "I wish I could read",
                )
        self.assertEqual(
                node.tag,
                "div",
                )
        self.assertEqual(
                node.value,
                "I wish I could read",
                )
        self.assertEqual(
                node.children,
                None,
                )
        self.assertEqual(
                node.props,
                None,
                )

    def test_repr(self):
        node = HTMLNode(
                "p",
                "What a strange world",
                None,
                {"class": "primary"},
                )
        self.assertEqual(
                node.__repr__(),
                "HTMLNode(tag:p, value:What a strange world, children:None, props:{'class': 'primary'})",
                )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "text", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "link", props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_all_defaults_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

if __name__=="__main__":
    unittest.main()
