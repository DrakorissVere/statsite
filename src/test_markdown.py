import unittest
from markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    md_to_html_nodes,
)
from htmlnode import LeafNode, ParentNode


class TestMarkdown(unittest.TestCase):
    def test_blocks(self):
        blocks = markdown_to_blocks("""This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
""")
        self.assertEqual(blocks[0], "This is **bolded** paragraph")
        self.assertEqual(blocks[1], """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""")
        self.assertEqual(blocks[2], """* This is a list
* with items""")

    def test_block_types(self):
        block = "## Some header"
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.HEADING)

        block = """```js
function a(b, c) { return b + c; }
```"""
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.CODE)

        block = """> quoting
> something"""
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.QUOTE)

        block = """* one
* two
* three"""
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.UNORDERED_LIST)

        block = """- one
- two
-three"""
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.UNORDERED_LIST)

        block = """1. one
2. two
3. three"""
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.ORDERED_LIST)

        block = """1. one
2. two
4. not ordered =|"""
        btype = block_to_block_type(block)
        self.assertNotEqual(btype, BlockType.ORDERED_LIST)

        block = "Just a **paragraph** block"
        btype = block_to_block_type(block)
        self.assertEqual(btype, BlockType.PARAGRAPH)

        def test_md_to_html_node(self):
            markdown = """# Markdown test
## Quoting

> This is a quote
> with multiple lines

## Unordered list

* Item 1
* Item 2
* Item 3

## Ordered list

1. Item 1
2. Item 2
3. Item 3

## Code block

```js
function add(a, b) {
    return a + b;
}
```

## Paragraph

This is a paragraph with **bold** and *italic* text, and `code` here."""
            nodes = md_to_html_nodes(markdown)
            expected = ParentNode("div", [
                LeafNode("h1", "Markdown test"),
                LeafNode("h2", "Quoting"),
                ParentNode("blockquote", [
                    LeafNode("p", "This is a quote"),
                    LeafNode("p", "with multiple lines"),
                ]),
                LeafNode("h2", "Unordered list"),
                ParentNode("ul", [
                    LeafNode("li", "Item 1"),
                    LeafNode("li", "Item 2"),
                    LeafNode("li", "Item 3"),
                ]),
                LeafNode("h2", "Ordered list"),
                ParentNode("ol", [
                    LeafNode("li", "Item 1"),
                    LeafNode("li", "Item 2"),
                    LeafNode("li", "Item 3"),
                ]),
                LeafNode("h2", "Code block"),
                ParentNode(
                    "pre", [LeafNode("code", "function add(a, b) {\n    return a + b;\n}")]),
                LeafNode("h2", "Paragraph"),
                ParentNode("p", [
                    LeafNode("p", "This is a paragraph with "),
                    LeafNode("strong", "bold"),
                    LeafNode("p", " and "),
                    LeafNode("em", "italic"),
                    LeafNode("p", " text, and "),
                    LeafNode("code", "code"),
                    LeafNode("p", " here."),
                ]),
            ])
            self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
