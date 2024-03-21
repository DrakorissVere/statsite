import os
import shutil
from markdown import md_to_html_nodes


def prepare_public():
    current_dir = os.getcwd()
    public_dir = os.path.join(current_dir, 'public')

    if not os.path.exists(public_dir):
        os.mkdir(public_dir)

    for filename in os.listdir(public_dir):
        file_path = os.path.join(public_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # static_dir = os.path.join(current_dir, 'static')
    # copy_static(static_dir, public_dir)


def copy_static(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.mkdir(d)
            copy_static(s, d)
        else:
            shutil.copy2(s, d)


def extract_title(markdown):
    title = None
    for line in markdown.split('\n'):
        if line.startswith('# '):
            title = line[2:]
            break
    if title is None:
        raise Exception('Title not found')
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} -> {dest_path}")
    markdown = open(from_path, 'r').read()
    template = open(template_path, 'r').read()
    title = extract_title(markdown)
    nodes = md_to_html_nodes(markdown)
    content = template.replace('{{ Title }}', title)
    content = content.replace('{{ Content }}', nodes.to_html())
    with open(dest_path, 'w') as f:
        f.write(content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(
            dest_dir_path, filename.replace('.md', '.html'))
        if os.path.isdir(file_path):
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursive(file_path, template_path, dest_path)
        else:
            generate_page(file_path, template_path, dest_path)


def main():
    prepare_public()
    generate_pages_recursive('content', 'template.html', 'public')
    # generate_page('index.md', 'template.html',
    #              'public/index.html')


main()
