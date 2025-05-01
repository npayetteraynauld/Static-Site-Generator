import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):

    def test_props_not_equal(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        test = node.props_to_html()
        example = ' href="https://www.google.com" target="_blank"'
        self.assertNotEqual(test, example)


    def test_props_are_equal(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        test = node.props_to_html()
        example = ' href="https://example.com" target="_blank"'
        self.assertEqual(test, example)

    def test_eq(self):
        node1 = HTMLNode(50, 40, 30)
        node2 = HTMLNode(value=50, tag=40, children=30)
        self.assertNotEqual(node1, node2)

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
 
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>") 

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_div_with_multiple_props(self):
        node = LeafNode("div", "Content", {"id": "main", "class": "container"})
        # Note: The order of properties might vary, so this might not always work
        self.assertEqual(node.to_html(), '<div id="main" class="container">Content</div>')

    def test_leaf_to_html_raises_error_for_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

    def test_to_html_with_2_children(self):
        child1 = LeafNode("n", "child1")
        child2 = LeafNode("m", "child2")
        parent_node = ParentNode("p", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<p><n>child1</n><m>child2</m></p>")

class TestTexttoHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_link(self):
        node = TextNode("anchor text", TextType.LINK, "https://hellomam.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props, {"href": "https://hellomam.com"})

    def test_IMAGE(self):
        node = TextNode("alt text", TextType.IMAGE, "https://hellopops.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://hellopops.com", "alt": "alt text"})
    
if __name__ == "__main__":
    unittest.main()
