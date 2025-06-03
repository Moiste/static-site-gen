import unittest
from blocktype import BlockType, block_to_block_type
from markdown_helper import (
    markdown_to_blocks,
    markdown_to_html_node)
class TestMarkDown(unittest.TestCase):
   
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


  def test_markdown_to_blocks_newlines(self):
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

  def test_heading_block(self):
    heading_md = block_to_block_type("# Heading 1")
    self.assertEqual(heading_md, BlockType.HEADING)

  def test_code_block(self):
    code_md = block_to_block_type("```\ndef foo():\n    pass\n```")
    self.assertEqual(code_md, BlockType.CODE)

  def test_quote_block(self):
    quote_md = block_to_block_type("> This is a quote.")
    self.assertEqual(quote_md, BlockType.QUOTE)

  def test_unordered_list_block(self):
    unordered_list_md = block_to_block_type("- Item 1\n- Item 2")
    self.assertEqual(unordered_list_md, BlockType.ULIST)

  def test_ordered_list_block(self):
    ordered_list_md = block_to_block_type("1. First\n2. Second")
    self.assertEqual(ordered_list_md, BlockType.OLIST)

  def test_block_to_block_types(self):
    block = "# heading"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    block = "```\ncode\n```"
    self.assertEqual(block_to_block_type(block), BlockType.CODE)
    block = "> quote\n> more quote"
    self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    block = "- list\n- items"
    self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    block = "1. list\n2. items"
    self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    block = "paragraph"
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


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

#   def test_codeblock(self):
#     md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

#     node = markdown_to_html_node(md)
#     html = node.to_html()
#     self.assertEqual(
#         html,
#         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
#     )
if __name__ == "__main__":
    unittest.main()