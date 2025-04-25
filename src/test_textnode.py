import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        print("Running test_eq2")
        node1 = TextNode("Hello", TextType.ITALIC, "url")
        node2 = TextNode("Hello", TextType.BOLD, "url")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
