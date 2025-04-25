import unittest

from htmlnode import *

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
 
    









if __name__ == "__main__":
    unittest.main()
