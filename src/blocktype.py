from enum import Enum

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  ULIST = "unordered_list"
  OLIST = "ordered_list"

def block_to_block_type(markdown):
  if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return BlockType.HEADING
  elif markdown.startswith("```") and markdown.endswith("```"):
    return BlockType.CODE
  elif markdown.startswith(">"):
    return BlockType.QUOTE
  elif markdown.startswith("- "):
    return BlockType.ULIST
  elif markdown.startswith("1. "):
    list_num = 1
    md_lines = markdown.split('\n')
    for line in md_lines:
      if not line.startswith(f"{list_num}. "):
        return BlockType.PARAGRAPH
      list_num += 1
    return BlockType.OLIST
  
  return BlockType.PARAGRAPH
  
