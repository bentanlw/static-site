from textnode import TextNode, TextType
from pathlib import Path
import shutil
import sys

from utils import generate_page, generate_pages_recursive

def copy_recursively(src, dst):
    for item in src.iterdir():
        if item.is_file():
            print(item)
            shutil.copy(item, dst/item.name)
        else:
            (dst/item.name).mkdir()
            copy_recursively(item, dst/item.name)

def main():
    basepath = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/")
    source_dir = basepath/"static"
    destination_dir = basepath/"docs"
    content_dir = basepath/"content"
    template_path = basepath/"template.html"

    if not source_dir.is_dir():
        raise Exception(f"Error: '{source_dir}' does not exist, nothing to copy")

    # clear out and create destination_dir if needed
    if destination_dir.is_dir():
        print(f"'{destination_dir}' exists. Deleting and creating afresh...")
        shutil.rmtree(destination_dir)
    destination_dir.mkdir(parents=True)

    copy_recursively(source_dir, destination_dir)
    generate_pages_recursive(content_dir, template_path, destination_dir, destination_dir)


if __name__ == "__main__":
    main()
