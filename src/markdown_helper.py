from textnode import TextType, TextNode
from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode, text_node_to_html_node

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
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
  lines = markdown.split("\n\n")
  filtered_lines = []
  for line in lines:
    if line == "":
      continue
    filtered_lines.append(line.strip())
  return filtered_lines

def text_to_child(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children

def paragraph_to_html_node(block):
  lines = block.split('\n')
  paragraph = " ".join(lines)
  children = text_to_child(paragraph)
  return ParentNode('p', children)

def heading_to_html_node(block):
  heading_level = 0
  for ch in block:
    if ch == '#':
      heading_level += 1
    else:
      break
  if heading_level + 1 >= len(block):
    raise ValueError(f"Invalid heading level: {heading_level}")
  text = block[heading_level + 1:]
  children = text_to_child(text)
  return ParentNode(f"h{heading_level}", children)
  
def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")
  text = block[4:-3]
  text_node = TextNode(text, TextType.TEXT)
  child = text_node_to_html_node(text_node)
  codetag = ParentNode("code", [child])
  return ParentNode("pre", [codetag]) 

def quote_to_html_node(block):
  lines = block.split('\n')
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    new_lines.append(line.lstrip('>').strip())
  content = " ".join(new_lines)
  children = text_to_child(content)
  return ParentNode("blockquote", children)

def ulist_to_html_node(block):
  items = block.split('\n')
  li_items = []
  for item in items:
    text = item[2:]
    children = text_to_child(text)
    li_items.append(ParentNode('li', children))
  return ParentNode("ul", li_items)

def olist_to_html_node(block):
  items = block.split('\n')
  li_items = []
  for item in items:
    text = item[3:]
    children = text_to_child(text)
    li_items.append(ParentNode('li', children))
  return ParentNode("ol", li_items)

def block_to_html_node(block):
  block_type = block_to_block_type(block)
  match block_type:
    case BlockType.PARAGRAPH:
      return paragraph_to_html_node(block)
    case BlockType.HEADING:
      return heading_to_html_node(block)
    case BlockType.CODE:
      return code_to_html_node(block)
    case BlockType.QUOTE:
      return quote_to_html_node(block)
    case BlockType.ULIST:
      return ulist_to_html_node(block)
    case BlockType.OLIST:
      return olist_to_html_node(block)
    case _:
      raise ValueError(f"Invalid block type {block}")

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children)

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 header found")
