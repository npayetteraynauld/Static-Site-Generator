import sys
import os
import shutil
import re

from block_to_html import markdown_to_html_node

def copy_static(static_dir, target_dir='docs'):
    """Copy all files from static_dir to target_dir."""
    if not os.path.exists(static_dir):
        return
        
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Copy all files and directories recursively
    for item in os.listdir(static_dir):
        src_path = os.path.join(static_dir, item)
        dst_path = os.path.join(target_dir, item)
        
        if os.path.isdir(src_path):
            # Recursively copy directory
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            # Copy file
            shutil.copy2(src_path, dst_path) 

def extract_title(markdown):
    extracted = re.match(r'^#\s+(.+)', markdown.strip())
    if not extracted:
        raise Exception("No title to extract")
    return extracted.group(1).strip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    directory = os.path.dirname(dest_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(full_html)

    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath='/'):
    list_folders = os.listdir(dir_path_content)
    for folder in list_folders:
        complete_path = os.path.join(dir_path_content, folder)
        public_path = os.path.join(dest_dir_path, folder)
        root, ext = os.path.splitext(public_path)
        if folder and os.path.isfile(complete_path) and ext == '.md':
            html_path = root + '.html'
            generate_page(complete_path, template_path, html_path, basepath)
        elif folder and os.path.isdir(complete_path):
            if not os.path.exists(public_path):
                os.makedirs(public_path)
            generate_pages_recursive(complete_path, template_path, public_path, basepath)
    return




def main():
    basepath = '/'
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs', exist_ok=True)
    copy_static('static')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)
    return

main()
