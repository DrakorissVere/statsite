import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_markdown_link,
    text_to_textnodes,
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

    def test_md_image(self):
        l = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)")
        self.assertEqual(l, [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ])

    def test_md_link(self):
        l = extract_markdown_links(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)")
        self.assertEqual(l, [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.com/some.png) and another ![second image](https://cats.com/alot.jpg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(nodes[0], TextNode(
            "This is text with an ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(
            "image", TextType.IMAGE, "https://i.com/some.png"))
        self.assertEqual(nodes[2], TextNode(
            " and another ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(
            "second image", TextType.IMAGE, "https://cats.com/alot.jpg"))

    def test_split_link(self):
        node = TextNode(
            "Some text with a [link-1](https://duckduckgo.com) and two [link 2](https://void.null)", TextType.TEXT)
        nodes = split_markdown_link([node])
        self.assertEqual(nodes[0], TextNode(
            "Some text with a ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(
            "link-1", TextType.LINK, "https://duckduckgo.com"))
        self.assertEqual(nodes[2], TextNode(
            " and two ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(
            "link 2", TextType.LINK, "https://void.null"))

    def test_text_to_nodes(self):
        txt = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(txt)
        self.assertEqual(nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("text", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" with an ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[4], TextNode(" word and a ", TextType.TEXT))
        self.assertEqual(nodes[5], TextNode("code block", TextType.CODE))
        self.assertEqual(nodes[6], TextNode(" and an ", TextType.TEXT))
        self.assertEqual(nodes[7], TextNode(
            "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(nodes[8], TextNode(" and a ", TextType.TEXT))
        self.assertEqual(nodes[9], TextNode(
            "link", TextType.LINK, "https://boot.dev"))


if __name__ == "__main__":
    unittest.main()
