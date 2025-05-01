import unittest

from split_delimiter import *
from blocks import markdown_to_blocks

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Check out [Boot.dev](https://boot.dev) for learning and [GitHub](https://github.com) for code hosting.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" for learning and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(" for code hosting.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning(self):
        node = TextNode(
            "[First link](https://example.com) followed by text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First link", TextType.LINK, "https://example.com"), 
                TextNode(" followed by text.", TextType.TEXT)
            ], 
            new_nodes
        )
    
    def test_split_links_at_end(self):
        node = TextNode(
            "Text followed by [last link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT), 
                TextNode("last link", TextType.LINK, "https://example.org")
            ], 
            new_nodes
        )
    
    def test_split_links_adjacent(self):
        node = TextNode(
            "Text with [link1](https://example1.com)[link2](https://example2.com) adjacent links.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example1.com"),
                TextNode("link2", TextType.LINK, "https://example2.com"),
                TextNode(" adjacent links.", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplit(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_split(self):
        markdown = "Paragraph one.\n\nParagraph two."
        expected = ["Paragraph one.", "Paragraph two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_newlines(self):
        markdown = "Para one.\n\n\n\nPara two."
        expected = ["Para one.", "Para two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_lines_within_block(self):
        markdown = "Line one\nLine two\n\nLine three\nLine four"
        expected = ["Line one\nLine two", "Line three\nLine four"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n  \n\t\n"), [])

    def test_no_double_newline(self):
        markdown = "This is a single paragraph with no breaks."
        expected = ["This is a single paragraph with no breaks."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
