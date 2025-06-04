import sys
from dir_helper import copy_src_to_dst_dir, generate_pages_recursive

src_dir = "./static"
build_dir = "./docs"

def main():
  base_path = sys.argv[1] if sys.argv[1] else '/' 
  copy_src_to_dst_dir(src_dir, build_dir)
  generate_pages_recursive(base_path=base_path, dir_path_content="./content", template_path="./template.html", dest_dir_path=build_dir)
  
main()