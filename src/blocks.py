from enum import Enum
import re

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    block_list = markdown.split("\n\n")
    clean_blocks = []

    for block in block_list:
        lines = block.split("\n")
        clean_lines = [line.strip() for line in lines]
        clean_block = "\n".join(clean_lines)

        if clean_block:
            clean_blocks.append(clean_block)

    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def is_quote_block(block):
    lines = block.split('\n')
    return all(line.strip().startswith('>') for line in lines if line.strip())

def is_unordered_list_block(block):
    lines = block.split("\n")
    return all(line.strip().startswith("- ") for line in lines if line.strip())

def is_ordered_list_block(block):
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    for i, line in enumerate(lines, start=1):
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            return False
    return True

def block_to_block_type(block):
    if re.match(r'^#{1,6} ', block) is not None:
        return BlockType.HEADING
    
    if re.fullmatch(r"```[\s\S]*?```", block) is not None:
        return BlockType.CODE
    
    if is_quote_block(block):
        return BlockType.QUOTE

    if is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST

    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH



