import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Another node", TextType.BOLD, "http://host.org")
        node2 = TextNode("Another node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("a cat", TextType.IMAGE,
                        "https://somehost.com/cat.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.props, {
            "src": "https://somehost.com/cat.png",
            "alt": "a cat"
        })

    def test_split_nodes(self):
        node = TextNode("Text with a `code block` delim", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result[0], TextNode("Text with a ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code block", TextType.CODE))
        self.assertEqual(result[2], TextNode(" delim", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()
