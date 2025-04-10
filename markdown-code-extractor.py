# markdown-code-extractor.py
# ---------------------------------------------
# This script extracts code blocks from a Markdown file and saves them
# as individual files in a specified output directory. The script detects
# the programming language of each code block (if specified) and assigns
# an appropriate file extension based on a predefined mapping.
#
# Usage:
#   python markdown-code-extractor.py <markdown_file> <output_directory>
#
# Example:
#   python markdown-code-extractor.py example.md output/
#
# Author: Sasank Vishnubhatla <svishnubhatla@cert.org>
# ---------------------------------------------

import re

# Global verbosity flag
VERBOSITY = False

# Safe maximum length for file names
MAX_FILENAME_LENGTH = 50

# Global template Makefile
TEMPLATE_MAKEFILE = """\
# Simple Makefile to compile each C script created by Markdown Code Extract
# This is generated from a template

CC := gcc
CFLAGS := -g3 -Wall -c -time -v --std=c2x

SRCS := $(wildcard *.c)
PROGS := $(patsubst %.c,%,$(SRCS))

all: $(PROGS)

# Rule to compile each C file
%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGS)

"""

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


def extract_code_blocks(markdown_text: str, verbosity=None) -> list[tuple[str, str, str]]:
    """
    Extracts all code blocks from a Markdown document using regex.

    Each code block is checked for a specified programming language.
    If no language is specified, it defaults to "plain".

    :param markdown_text: The Markdown content as a string.
    :param verbosity: Optional argument to enable verbose mode.
    :return: A list of tuples where each tuple contains:
             - The detected code type (language)
             - The extracted code content
    """
    code_blocks = []
    current_heading = "__no_heading__"

    # define regex patterns
    code_block_pattern = re.compile(
        r'``` ([a-zA-Z0-9_-]*)\n(.*?)```', re.DOTALL)
    heading_pattern = re.compile(r'^(#+)\s+(.*)', re.MULTILINE)

    # find all matches
    matches = list(heading_pattern.finditer(markdown_text)) + \
        list(code_block_pattern.finditer(markdown_text))
    matches.sort(key=lambda match: match.start())

    for match in matches:
        if match.re == heading_pattern:
            current_heading = match.group(2).strip().lower().replace(' ', '_')

        elif match.re == code_block_pattern:
            code_type = match.group(1).strip(
            ).lower() if match.group(1) else "plain"
            code_content = match.group(2).strip()
            code_blocks.append((code_type, code_content, current_heading))

    if VERBOSITY or (verbosity == True):
        print(
            f"Found {len(code_blocks)} code blocks of file types {set(map(lambda cb: cb[0]))}")

    return code_blocks


def save_code_blocks(code_blocks: list[tuple[str, str, str]], output_dir: str, verbosity=None):
    """
    Saves each extracted code block as a separate file in the output directory.

    The function assigns an appropriate file extension based on the detected
    programming language. If no known language is found, a default `.txt`
    extension is used.

    :param code_blocks: A list of tuples containing (code type, code content).
    :param output_dir: The directory where extracted code blocks will be saved.
    :param verbosity: Optional argument to enable verbose mode.
    """
    import os
    import shutil
    os.makedirs(output_dir, exist_ok=True)

    # write template Makefile to output_dir/Makefile
    makefile_dest = os.path.join(output_dir, "Makefile")
    with open(makefile_dest, "w", encoding="utf-8") as makefile:
        makefile.write(TEMPLATE_MAKEFILE)

    for i, (code_type, block, heading) in enumerate(code_blocks, 1):
        file_extension = LANGUAGE_EXTENSIONS.get(code_type, "txt")

        # add padding to i
        pad_length = len(str(len(code_blocks) + 1))
        padded_i = str(i).rjust(pad_length, "0")

        # sanitize heading for file name
        sanitized_name_full = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", heading)

        # build file name and truncate if necessary
        file_name_tail = f"_block_{padded_i}"
        max_sanitized_length = MAX_FILENAME_LENGTH - len(file_name_tail)
        sanitized_name = sanitized_name_full[:max_sanitized_length]
        file_name = sanitized_name + file_name_tail

        file_path = os.path.join(
            output_dir, f"{file_name}.{file_extension}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(block + "\n")

        if VERBOSITY or (verbosity == True):
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
    import argparse
    parser = argparse.ArgumentParser(
        description="Extract code blocks from a Markdown file and save them to an output directory.")
    parser.add_argument("filename", type=str, help="Path to the Markdown file")
    parser.add_argument("output_dir", type=str,
                        help="Directory to save extracted code blocks")
    parser.add_argument("-v", "--verbose", action="store_true",
                        default=False, help="Enable verbose mode")

    args = parser.parse_args()

    VERBOSITY = args.verbose

    # Read Markdown content
    with open(args.filename, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    if VERBOSITY:
        print(f"Read Markdown file {args.filename}")

    code_blocks = extract_code_blocks(markdown_content, VERBOSITY)

    save_code_blocks(code_blocks, args.output_dir, VERBOSITY)


if __name__ == "__main__":
    main()
