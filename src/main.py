from textnode import TextNode, TextType
from pathlib import Path
import shutil

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
    cwd = Path.cwd()
    source_dir = Path("static")
    destination_dir = Path("public")
    content_dir = Path("content")

    if not source_dir.is_absolute():
        print(f"'{source_dir}' is a relative path. Converting...")
        source_dir = source_dir.resolve()
    if not destination_dir.is_absolute():
        print(f"'{destination_dir}' is a relative path. Converting...")
        destination_dir = destination_dir.resolve()

    if not source_dir.is_relative_to(cwd):
        raise Exception(f"Error: '{source_dir}' directory is not in project folder")
    if not destination_dir.is_relative_to(cwd):
        raise Exception(f"Error: '{destination_dir}' directory is not in project folder")

    if not source_dir.is_dir():
        raise Exception(f"Error: '{source_dir} does not exist, nothing to copy")

    # clear out and create destination_dir if needed
    if destination_dir.is_dir():
        print(f"'{destination_dir}' exists. Deleting and creating afresh...")
        shutil.rmtree(destination_dir)
    destination_dir.mkdir(parents=True)

    copy_recursively(source_dir, destination_dir)
    generate_pages_recursive(content_dir, "template.html", destination_dir)


if __name__ == "__main__":
    main()
