from textnode import TextNode, TextType
from dir_helper import copy_src_to_dst_dir, generate_pages_recursive

def main():
  copy_src_to_dst_dir("./static", "./public")
  generate_pages_recursive(dir_path_content="./content", template_path="./template.html", dest_dir_path="./public")
  # generate_page(from_path="./content/index.md", template_path="./template.html", dest_path="./public/index.html")
main()