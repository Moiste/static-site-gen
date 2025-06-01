import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("this is a text node", TextType.BOLD)
    node2 = TextNode("this is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_not_eq(self):
    node = TextNode("this is a text node", TextType.BOLD)
    node2 = TextNode("this is also a text node", TextType.TEXT)
    self.assertNotEqual(node, node2)

if __name__ == "__main__":
  unittest.main()