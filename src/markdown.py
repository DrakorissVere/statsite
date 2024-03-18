from enum import Enum
import re
from htmlnode import LeafNode, ParentNode


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


def md_to_html_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            level = 0
            while block[level] == "#":
                level += 1
            nodes.append(LeafNode(f"h{level}", block[level+1:].strip()))
        elif btype == BlockType.CODE:
            parent = ParentNode("pre", [])
            code = LeafNode("code", block[3:-3].strip())
            parent.children.append(code)
            nodes.append(parent)
        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            nodes.append(ParentNode("blockquote", [LeafNode("p", lines[0][2:].strip(
            ))] + [LeafNode("p", line[2:].strip()) for line in lines[1:]]))
        elif btype == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            nodes.append(ParentNode(
                "ul", [ParentNode("li", [LeafNode("p", line[2:].strip())]) for line in lines]))
        elif btype == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            nodes.append(ParentNode(
                "ol", [ParentNode("li", [LeafNode("p", line[3:].strip())]) for line in lines]))
        else:
            nodes.append(LeafNode("p", block))

    root = ParentNode("div", nodes)
    root.children = nodes
    return root
