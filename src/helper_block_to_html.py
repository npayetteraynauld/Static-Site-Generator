from htmlnode import HTMLNode, LeafNode, ParentNode
from split_delimiter import text_to_textnodes
from textnode import text_node_to_html_node
import re

def get_paragraph_children(text):
    lines = text.splitlines()
    removed_newline = " ".join(lines)
    children = [text_node_to_html_node(node) for node in text_to_textnodes(removed_newline)]
    return children

def get_heading_text(text):
    return text.lstrip("#").lstrip()

def get_heading_level(text):
    return len(text) - len(text.lstrip("#"))

def get_code_children_node(text):
    lines = text.splitlines()
    content = "\n".join(lines[1:-1])
    content = content + "\n"
    return LeafNode(tag="code", value=content)

def get_quote_children(text):
    lines = text.splitlines()
    children = []
    for i, line in enumerate(lines):
        clean_line = line[1:].lstrip()
        nodes = [text_node_to_html_node(node) for node in text_to_textnodes(clean_line)]
        children.extend(nodes)
        if i < len(lines) - 1:
            children.append(LeafNode(tag="br", value=""))
    return children

def get_unordered_list_children(text):
    lines = text.splitlines()
    children = []
    for line in lines:
        clean_line = line[1:].lstrip()
        nodes = [text_node_to_html_node(node) for node in text_to_textnodes(clean_line)]
        children.append(ParentNode(tag="li", children=nodes))

    return children

def get_ordered_list_children(text):
    lines = text.splitlines()
    children = []
    for line in lines:
        clean_line = re.sub(r'^\d+\.', '', line).lstrip()
        nodes = [text_node_to_html_node(node) for node in text_to_textnodes(clean_line)]
        children.append(ParentNode(tag="li", children=nodes))

    return children
        


        
