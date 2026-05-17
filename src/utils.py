from block import BlockType, block_to_block_type
from parentnode import ParentNode
from textnode import TextType, TextNode
from leafnode import LeafNode
from pathlib import Path
import re

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
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        original_text = old_node.text
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        original_text = old_node.text
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image([old_node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    return new_nodes

def text_to_children(text):
    textnodes_list = text_to_textnodes(text)
    leafnodes_list = []
    for textnode in textnodes_list:
        leafnodes_list.append(text_node_to_html_node(textnode))
    return leafnodes_list

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        else:
            blocks.append(block.strip())
    return blocks

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            child_nodes = text_to_children(block.replace("\n", " "))
            return ParentNode("p", child_nodes)
        case BlockType.HEADING:
            # determine heading type based on number of #
            heading = re.search(r"(^#{1,6}) (.+)", block)
            tag = f"h{len(heading.group(1))}"
            child_nodes = text_to_children(heading.group(2))
            return ParentNode(tag, child_nodes)
        case BlockType.CODE:
            code = LeafNode("code", block.replace("```", "").strip())
            return ParentNode("pre", [code])
        case BlockType.QUOTE:
            child_nodes = text_to_children(block.replace(">", "").strip())
            return ParentNode("blockquote", child_nodes)
        case BlockType.UNORDERED_LIST:
            grandchild_block = block.split("- ")
            children = []
            for grandchild in grandchild_block:
                if len(grandchild) == 0:
                    continue
                children.append(ParentNode("li", text_to_children(grandchild.strip())))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            grandchild_block = block.splitlines()
            children = []
            for grandchild in grandchild_block:
                text =  re.search(r"^\d+. (.*)", grandchild)
                children.append(ParentNode("li", text_to_children(text.group(1).strip())))
            return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        blocks_list.append(block_to_html_node(block, block_type))
    return ParentNode("div", blocks_list)

def extract_title(markdown):
    heading = re.search(r"^#{1} (.+)", markdown)
    if not heading:
        raise Exception("No h1 heading found!")
    return heading.group(1)

def generate_page(from_path, template_path, dest_path, docs_root):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
    with open(from_path, 'r') as f:
        from_file = f.read()
    with open(template_path, 'r') as f:
        template_file = f.read()
    html_content = markdown_to_html_node(from_file).to_html()
    from_title = extract_title(from_file)
    output_file = Path(dest_path).resolve()
    depth = len(output_file.parent.relative_to(Path(docs_root).resolve()).parts)
    prefix = "/".join([".."] * depth) if depth > 0 else "."
    template_file = template_file.replace("{{ Title }}", from_title)
    template_file = template_file.replace("{{ Content }}", html_content)
    template_file = template_file.replace("href=\"/", f"href=\"{prefix}/")
    template_file = template_file.replace("src=\"/", f"src=\"{prefix}/")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, 'w') as f:
        f.write(template_file)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, docs_root):
    for item in dir_path_content.iterdir():
        if item.is_file() and item.suffix == ".md":
            dest_path = dest_dir_path/item.with_suffix(".html").name
            generate_page(item, template_path, dest_path, docs_root)
        elif item.is_dir():
            generate_pages_recursive(item, template_path, dest_dir_path/item.name, docs_root)

