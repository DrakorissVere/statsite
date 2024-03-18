from htmlnode import LeafNode
from enum import Enum
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text \
            and self.text_type == other.text_type \
            and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", props={
            "src": text_node.url,
            "alt": text_node.text
        })

    raise Exception("unknown text node")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"no matching closing '{delimiter}' symbol")

        for i in range(len(parts)):
            part = parts[i]
            if part == "":
                continue
            ty = TextType.TEXT if i % 2 == 0 else text_type
            result.append(TextNode(part, ty))

    return result


def extract_markdown_images(text):
    pattern = r"!\[(.+?)\]\((.+?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[(.+?)\]\((.+?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) < 1:
            result.append(node)
            continue

        txt = node.text
        for t in images:
            parts = txt.split(f"![{t[0]}]({t[1]})", 1)
            if len(parts) == 2:
                result.append(TextNode(parts[0], TextType.TEXT))
                result.append(TextNode(t[0], TextType.IMAGE, t[1]))
            else:
                result.append(TextNode(parts[0], TextType.TEXT))
                break
            txt = parts[1]
        if txt != "":
            result.append(TextNode(txt, TextType.TEXT))

    return result


def split_markdown_link(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_links(node.text)
        if len(images) < 1:
            result.append(node)
            continue

        txt = node.text
        for t in images:
            parts = txt.split(f"[{t[0]}]({t[1]})", 1)
            if len(parts) == 2:
                result.append(TextNode(parts[0], TextType.TEXT))
                result.append(TextNode(t[0], TextType.LINK, t[1]))
            else:
                result.append(TextNode(parts[0], TextType.TEXT))
                break
            txt = parts[1]

    return result


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_markdown_link(result)
    return result
