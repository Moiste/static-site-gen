import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
      node = HTMLNode(
          "div",
          "Hello, world!",
          None,
          {"class": "greeting", "href": "https://boot.dev"},
      )
      self.assertEqual(
          node.props_to_html(),
          ' class="greeting" href="https://boot.dev"',
      )

    def test_values(self):
      node = HTMLNode(
          "div",
          "I wish I could read",
      )
      self.assertEqual(
          node.tag,
          "div",
      )
      self.assertEqual(
          node.value,
          "I wish I could read",
      )
      self.assertIsNone(
          node.children
      )
      self.assertIsNone(
          node.props
      )

    def test_repr(self):
      node = HTMLNode(
          "p",
          "What a strange world",
          None,
          {"class": "primary"},
      )
      self.assertEqual(
          node.__repr__(),
          "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
      )

    def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_tags(self):
      node = LeafNode("h1", "Hello me!")
      self.assertEqual(node.to_html(), "<h1>Hello me!</h1>")

    def test_leaf_to_html_special_characters(self):
      node = LeafNode("span", "<Hello & Goodbye>")
      self.assertEqual(node.to_html(), "<span><Hello & Goodbye></span>")

    def test_leaf_to_html_numeric_content(self):
      node = LeafNode("li", "12345")
      self.assertEqual(node.to_html(), "<li>12345</li>")

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

    def test_to_html_with_nested_parents(self):
      grandchild_node = LeafNode("b", "grandchild")
      child_node = ParentNode("span", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      grandparent_node = ParentNode("div", [parent_node])
      self.assertEqual(
          grandparent_node.to_html(),
          "<div><div><span><b>grandchild</b></span></div></div>",
      )

    def test_to_html_with_multiple_child(self):
      grandchild_node1 = LeafNode("b", "grandchild1")
      grandchild_node2 = LeafNode("p", "grandchild2")
      grandchild_node3 = LeafNode("h2", "grandchild3")
      child_node1 = ParentNode("span", [grandchild_node1])
      child_node2 = ParentNode("h1", [grandchild_node2])
      child_node3 = ParentNode("p", [grandchild_node3])
      parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
      grandparent_node = ParentNode("div", [parent_node])
      self.assertEqual(
          grandparent_node.to_html(),
          "<div><div><span><b>grandchild1</b></span><h1><p>grandchild2</p></h1><p><h2>grandchild3</h2></p></div></div>",
      )

    def test_deeply_nested_structure(self):
      deep = LeafNode("em", "very deep")
      inner = ParentNode("strong", [deep])
      middle = ParentNode("span", [inner])
      outer = ParentNode("section", [middle])
      self.assertEqual(outer.to_html(), "<section><span><strong><em>very deep</em></strong></span></section>")

    def test_html_special_characters(self):
      leaf = LeafNode("p", "5 < 6 & 7 > 4")
      self.assertEqual(leaf.to_html(), "<p>5 < 6 & 7 > 4</p>")


class TestTextNodeToHTMLNode(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertIsNone(html_node.tag)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold_text(self):
    node = TextNode("Bold text", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "Bold text")

  def test_italic_text(self):
    node = TextNode("Italic text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "Italic text")

  def test_code_text(self):
    node = TextNode("Code text", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "Code text")

  def test_link_text(self):
    node = TextNode("OpenAI", TextType.LINK, url="https://openai.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "OpenAI")
    self.assertEqual(html_node.props.get("href"), "https://openai.com")

  def test_image_text_node(self):
    node = TextNode("OpenAI logo", TextType.IMAGE, url="https://openai.com/logo.png")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.props.get("src"), "https://openai.com/logo.png")
    self.assertEqual(html_node.props.get("alt"), "OpenAI logo")

if __name__ == "__main__":
    unittest.main()