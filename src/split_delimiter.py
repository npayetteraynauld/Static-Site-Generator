from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        while delimiter in remaining_text:
            first_delimiter_pos = remaining_text.find(delimiter)
            
            second_delimiter_pos = remaining_text.find(delimiter, first_delimiter_pos + len(delimiter))
            if second_delimiter_pos == -1:
                raise Exception(f"No closing delimiter found for '{delimiter}'")
            
            if first_delimiter_pos > 0:
                new_nodes.append(TextNode(remaining_text[:first_delimiter_pos], TextType.TEXT))
            
            text_between = remaining_text[first_delimiter_pos + len(delimiter):second_delimiter_pos]
            new_nodes.append(TextNode(text_between, text_type))
            
            remaining_text = remaining_text[second_delimiter_pos + len(delimiter):]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = current_text.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], old_node.text_type))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, old_node.text_type))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        for link_alt, link_url in links:
            link_markdown = f"[{link_alt}]({link_url})"
            parts = current_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], old_node.text_type))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, old_node.text_type))

    return new_nodes

       
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_italic = split_nodes_delimiter(nodes_bold, "_", TextType.ITALIC)
    nodes_code = split_nodes_delimiter(nodes_italic, "`", TextType.CODE)
    nodes_link = split_nodes_link(nodes_code)
    nodes_image = split_nodes_image(nodes_link)
    return nodes_image





