from blocks import *
from helper_block_to_html import get_heading_text, get_ordered_list_children, get_paragraph_children, get_quote_children, get_code_children_node, get_heading_level, get_unordered_list_children
from htmlnode import *
from split_delimiter import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes= []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children_nodes.append(ParentNode(tag="p", children=get_paragraph_children(block)))

        elif block_type == BlockType.HEADING:
            children_nodes.append(ParentNode(tag=f"h{get_heading_level(block)}", children=[text_node_to_html_node(node) for node in text_to_textnodes(get_heading_text(block))]))

        elif block_type == BlockType.CODE:
            children_nodes.append(ParentNode(tag="pre", children=[get_code_children_node(block)]))

        elif block_type == BlockType.QUOTE:
            children_nodes.append(ParentNode(tag="blockquote", children=get_quote_children(block)))

        elif block_type == BlockType.UNORDERED_LIST:
            children_nodes.append(ParentNode(tag="ul", children=get_unordered_list_children(block)))

        elif block_type == BlockType.ORDERED_LIST:
            children_nodes.append(ParentNode(tag="ol", children=get_ordered_list_children(block)))

            

    final_node = ParentNode(tag="div", children=children_nodes)
    return final_node
