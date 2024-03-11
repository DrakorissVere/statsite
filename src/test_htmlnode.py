import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("a", "some link", None, {
                        "href": "https://duckduckgo.com", "target": "_blank"})
        props = node.props_to_html()
        self.assertEqual(
            props, " href=\"https://duckduckgo.com\" target=\"_blank\"")

    def test_leaf_node(self):
        leaf = LeafNode("a", "some link", {
            "href": "https://duckduckgo.com"
        })
        html = leaf.to_html()
        self.assertEqual(
            html, "<a href=\"https://duckduckgo.com\">some link</a>")

    def test_parent_node(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "bald"),
                LeafNode(None, " text")
            ]
        )
        html = parent.to_html()
        self.assertEqual(html, "<p><b>bald</b> text</p>")


if __name__ == "__main__":
    unittest.main()
