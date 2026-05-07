from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text, tag=None)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextType.LINK:
            return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for n in old_nodes:
        # n.text gives me the string, delimiter is what i will use to split the string, text_type is used for whatever is within the delimiters, the rest retains the old text_type
        if n.text_type != TextType.TEXT:
            split_nodes.append(n)
        else:
            s = n.text.split(delimiter)
            if len(s)%2 == 0:
                raise Exception("invalid Markdown syntax")
            for i in range(0,len(s)):
                if i%2 != 0 and s[i]:
                    split_nodes.append(TextNode(s[i], text_type))
                elif s[i]:
                    split_nodes.append(TextNode(s[i], TextType.TEXT))
    return split_nodes
