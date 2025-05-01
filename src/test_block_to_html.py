import unittest
from block_to_html import markdown_to_html_node
from htmlnode import ParentNode

class TestBlocktoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph(self):
        md = "This is a paragraph."
        node = markdown_to_html_node(md)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertIn("This is a paragraph", str(node))

    def test_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertIn("Heading 1", str(node))

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertIn("print('hello')", str(node))

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "blockquote")
        self.assertIn("This is a quote", str(node))

    def test_unordered_list(self):
        md = "- item 1\n- item 2"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertIn("item 1", str(node))
        self.assertIn("item 2", str(node))

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "ol")
        self.assertIn("First", str(node))
        self.assertIn("Second", str(node))

    def test_mixed_blocks(self):
        md = "# Title\n\nParagraph text.\n\n- List item"
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")
