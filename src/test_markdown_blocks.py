import unittest
from blocktype import BlockType, block_to_block_type
from markdown_helper import (
    markdown_to_blocks)
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

  def test_block_to_block_type_values(self):
    heading_md = block_to_block_type("# Heading 1")
    self.assertEqual(
      heading_md,
      BlockType.HEADING
    )
if __name__ == "__main__":
    unittest.main()