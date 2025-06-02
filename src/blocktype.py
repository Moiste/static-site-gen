from enum import Enum

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
  if markdown[:2] == "# ":
    return BlockType.HEADING
  elif markdown[:3] == '```' and markdown[-3:] == '```':
    return BlockType.CODE
  elif markdown[0] == ">":
    return BlockType.QUOTE
  elif markdown[:2] == "- ":
    return BlockType.UNORDERED_LIST
  
  return BlockType.PARAGRAPH
  
