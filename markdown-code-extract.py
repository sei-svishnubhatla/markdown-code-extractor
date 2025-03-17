# markdown-code-extract.py
# ---------------------------------------------
# This script extracts code blocks from a Markdown file and saves them
# as individual files in a specified output directory. The script detects
# the programming language of each code block (if specified) and assigns
# an appropriate file extension based on a predefined mapping.
#
# Usage:
#   python markdown-code-extract.py <markdown_file> <output_directory>
#
# Example:
#   python markdown-code-extract.py example.md output/
#
# Author: Sasank Vishnubhatla <sasank@vishnubhatlas.net>
# ---------------------------------------------

import argparse
import os
import re

# Mapping of common programming languages to file extensions
LANGUAGE_EXTENSIONS = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "cs": "cs",
        "html": "html",
        "css": "css",
        "json": "json",
        "yaml": "yaml",
        "xml": "xml",
        "bash": "sh",
        "shell": "sh",
        "powershell": "ps1",
        "php": "php",
        "ruby": "rb",
        "swift": "swift",
        "go": "go",
        "r": "r",
        "perl": "pl",
        "kotlin": "kt",
        "rust": "rs",
        "dart": "dart",
        "lua": "lua",
        "makefile": "mk"
        }

def extract_code_blocks(markdown_text: str) -> list[tuple[str, str]]:
    """
    Extracts all code blocks from a Markdown document using regex.

    Each code block is checked for a specified programming language.
    If no language is specified, it defaults to "plain".

    :param markdown_text: The Markdown content as a string.
    :return: A list of tuples where each tuple contains:
             - The detected code type (language)
             - The extracted code content
    """
    code_blocks = []

    # NOTE: it looks like ``` lang is used consistently
    code_block_pattern = re.compile(r'``` ([a-zA-Z0-9_-]*)\n(.*?)```', re.DOTALL)

    for match in code_block_pattern.finditer(markdown_text):
        code_type = match.group(1).strip().lower() if match.group(1) else "plain"
        code_content = match.group(2).strip()
        code_blocks.append((code_type, code_content))

    return code_blocks

def save_code_blocks(code_blocks: list[tuple[str, str]], output_dir: str):
    """
    Saves each extracted code block as a separate file in the output directory.

    The function assigns an appropriate file extension based on the detected
    programming language. If no known language is found, a default `.txt`
    extension is used.

    :param code_blocks: A list of tuples containing (code type, code content)
    :param output_dir: The directory where extracted code blocks will be saved
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, (code_type, block) in enumerate(code_blocks, 1):
        file_extension = LANGUAGE_EXTENSIONS.get(code_type, "txt")
        file_path = os.path.join(output_dir, f"code_block_{i}.{file_extension}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(block)
        print(f"Saved Code Block {i} ({code_type}) to {file_path}")

def main():
    """
    Main function to handle command-line arguments and process the Markdown file.

    This function:
    1. Parses command-line arguments.
    2. Reads the specified Markdown file.
    3. Extracts code blocks from the file.
    4. Saves extracted code blocks to the specified output directory.
    """
    parser = argparse.ArgumentParser(description="Extract code blocks from a Markdown file and save them to an output directory.")
    parser.add_argument("filename", type=str, help="Path to the Markdown file")
    parser.add_argument("output_dir", type=str, help="Directory to save extracted code blocks")
    args = parser.parse_args()

    with open(args.filename, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    code_blocks = extract_code_blocks(markdown_content)

    save_code_blocks(code_blocks, args.output_dir)

if __name__ == "__main__":
    main()

