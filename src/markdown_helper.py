from textnode import TextType, TextNode
from blocktype import block_to_block_type, block_to_html_node, BlockType
from htmlnode import ParentNode, LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    parts = node.text.split(delimiter)
    # no matching delimiters
    if len(parts) % 2 == 0:
      raise ValueError(f"Unmatched delimiter '{delimiter}' in text: '{node.text}'")
    
    for i, part in enumerate(parts):
      if part == "":
        continue
      # Text Type
      if i % 2 == 0:
        new_nodes.append(TextNode(part, TextType.TEXT))
      # Delimited Type
      else:
        new_nodes.append(TextNode(part, text_type))
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    text = node.text
    images_data = extract_markdown_images(node.text)
    idx = 0

    for alt, url in images_data:
      delimiter = f"![{alt}]({url})"
      split_idx = text.find(delimiter, idx)

      # Add text node before image
      if split_idx > idx:
        new_nodes.append(TextNode(text[idx:split_idx], TextType.TEXT))
      
      # Add image text node
      new_nodes.append(TextNode(alt, TextType.IMAGE, url))
      idx = split_idx + len(delimiter)
    
    # Append remaining text
    if idx < len(text):
      new_nodes.append(TextNode(text[idx:], TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    text = node.text
    images_data = extract_markdown_links(node.text)
    idx = 0

    for alt, url in images_data:
      delimiter = f"[{alt}]({url})"
      split_idx = text.find(delimiter, idx)

      # Add text node before image
      if split_idx > idx:
        new_nodes.append(TextNode(text[idx:split_idx], TextType.TEXT))
      
      # Add image text node
      new_nodes.append(TextNode(alt, TextType.LINK, url))
      idx = split_idx + len(delimiter)
    
    # Append remaining text
    if idx < len(text):
      new_nodes.append(TextNode(text[idx:], TextType.TEXT))
  return new_nodes

def text_to_textnodes(text):
  node_list = [TextNode(text, TextType.TEXT)]
  node_list = split_nodes_image(node_list)
  node_list = split_nodes_link(node_list)
  node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
  node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
  node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
  return node_list

def markdown_to_blocks(markdown):
  lines = markdown.split("\n\n")
  filtered_lines = []
  for line in lines:
    if line == "":
      continue
    filtered_lines.append(line.strip())
  return filtered_lines

def block_to_html_node(text_nodes):
  for node in text_nodes:
    block_type = block_to_block_type(node.text)
    text_type = node.text_type
    html_node = None
    match block_type:
      case BlockType.PARAGRAPH:
        match text_type:
          case TextType.TEXT:
            html_node = LeafNode("p", node.text).to_html()
          case TextType.BOLD:
            html_node = LeafNode("b", node.text).to_html()
          case TextType.CODE:
            html_node = LeafNode("code", node.text).to_html()
          case TextType.ITALIC:
            html_node = LeafNode("i", node.text).to_html()

  
  return html_node



def markdown_to_html_node(markdown):
  html_node = ParentNode("div", children=None)
  blocks = text_to_textnodes(markdown)
  # print(blocks)
  block_to_html_node(blocks)
  # for block in blocks:
    # print(block)
    # print(block_type)
    # print(block.text_type)
