import os
import shutil
from markdown_helper import markdown_to_html_node, extract_title

def copy_src_to_dst_dir(src_path, dst_path):
  if not os.path.exists(src_path):
    raise OSError(f"Source Path doesn't exist! {src_path}")  
  if os.path.exists(dst_path):
    shutil.rmtree(dst_path)

  copy_dir_recursive(src_path, dst_path)

def copy_dir_recursive(src_path, dst_path):
  if not os.path.exists(dst_path):
    os.mkdir(dst_path)

  for item in os.listdir(src_path):
    src_item = os.path.join(src_path, item)
    dst_item = os.path.join(dst_path, item)

    if os.path.isdir(src_item):
      copy_dir_recursive(src_item, dst_item)
    else:
      shutil.copy(src_item, dst_item)

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  with open(from_path) as md_file, open(template_path) as template_file:
    md_content = md_file.read()
    template_content = template_file.read()
  md_html = markdown_to_html_node(md_content).to_html()
  title = extract_title(md_content)
  template_content = template_content.replace("{{ Title }}", title)
  template_content = template_content.replace("{{ Content }}", md_html)

  with open(dest_path, 'w') as html_page:
    html_page.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for item in os.listdir(dir_path_content):
    src_item = os.path.join(dir_path_content, item)
    dst_item = os.path.join(dest_dir_path, item)
    if os.path.isdir(src_item):
      if not os.path.exists(dst_item):
        os.mkdir(dst_item)
      generate_pages_recursive(src_item, template_path, dst_item)
    elif src_item.endswith(".md"):
      dst_item = dst_item.replace(".md", ".html")
      generate_page(src_item, template_path, dst_item)