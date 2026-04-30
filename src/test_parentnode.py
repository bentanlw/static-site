import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        parent = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(parent.to_html(), "<p><b>bold</b> and <i>italic</i></p>")

    def test_props_on_parent(self):
        parent = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><p>text</p></div>')

    def test_no_children_raises(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_none_children_raises(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_no_tag_raises(self):
        parent = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_deep_nesting(self):
        # three levels deep
        inner = LeafNode("b", "deep")
        level2 = ParentNode("span", [inner])
        level1 = ParentNode("div", [level2])
        root = ParentNode("section", [level1])
        self.assertEqual(
            root.to_html(),
            "<section><div><span><b>deep</b></span></div></section>",
        )

    def test_mixed_children(self):
        # mix of ParentNode and LeafNode siblings
        parent = ParentNode("div", [
            LeafNode("p", "first"),
            ParentNode("ul", [
                LeafNode("li", "item1"),
                LeafNode("li", "item2"),
            ]),
            LeafNode("p", "last"),
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><p>first</p><ul><li>item1</li><li>item2</li></ul><p>last</p></div>",
        )

    def test_props_inherited_only_on_parent(self):
        # props on parent should not bleed into children
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"id": "main"})
        html = parent.to_html()
        self.assertIn('id="main"', html)
        self.assertEqual(html.count('id='), 1)
