from textnode import TextType, TextNode

class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self):
    if self.props is None:
      return ""
    
    html_val = []
    for key, val in self.props.items():
      html_val.append(f' {key}="{val}"')
    return "".join(html_val)

  def __repr__(self):
    return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
  
class LeafNode(HTMLNode):
  def __init__(self, tag=None, value=None, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("All leaf nodes must have a value")
    elif not self.tag:
      return str(self.value)
    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if not self.tag:
      raise ValueError("No tag found in ParentNode!")
    if not self.children:
      raise ValueError("No children found in ParentNode!")
    child_html = ""
    for child in self.children:
      child_html += child.to_html()

    return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'

def text_node_to_html_node(text_node):
  match (text_node.text_type):
    case TextType.TEXT:
      return LeafNode(None, value=text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
  raise ValueError(f"invalid text type: {text_node.text_type}")