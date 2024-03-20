from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    parts = markdown.split("\n")
    buf = []
    res = []

    for part in parts:
        if part == "":
            res.append("\n".join(buf))
            buf = []
            continue
        buf.append(part.strip())

    if len(buf) > 0:
        res.append("\n".join(buf))

    return res


def block_to_block_type(block):
    if re.match(r"^#{1,6} .+", block) is not None:
        return BlockType.HEADING

    if re.match(r"^```(?:[^\n]+)?\n((?:.*\n)*?)```$", block) is not None:
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("*") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST

    last = None
    ordered = True
    for line in lines:
        match = re.match(r"^(\d)\..+", line)

        if match is None:
            ordered = False
            break

        if last is not None:
            if last != int(match.group(1)) - 1:
                ordered = False
                break
        last = int(match.group(1))

    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def md_to_html_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            level = 0
            while block[level] == "#":
                level += 1
            nodes.append(ParentNode(
                f"h{level}", text_to_children(block[level+1:].strip())))
        elif btype == BlockType.CODE:
            parent = ParentNode("pre", [])
            code = ParentNode("code", text_to_children(block[3:-3].strip()))
            parent.children.append(code)
            nodes.append(parent)
        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            nodes.append(ParentNode("blockquote", text_to_children(
                "\n".join([line[2:] for line in lines]))))
        elif btype == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            nodes.append(ParentNode(
                "ul", [ParentNode("li", text_to_children(line[2:])) for line in lines]))
        elif btype == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            nodes.append(ParentNode(
                "ol", [ParentNode("li", text_to_children(line[3:])) for line in lines]))
        else:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            childs = text_to_children(paragraph)
            nodes.append(ParentNode("p", childs))

    root = ParentNode("div", nodes)
    root.children = nodes
    return root
