# Markdown Code Extractor

This project provides a script to extract code blocks from a Markdown file and save them as individual files in a specified output directory. The script detects the programming language of each code block (if specified) and assigns an appropriate file extension based on a predefined mapping.

## Usage

To use the script, run the following command:

```bash
python markdown-code-extract.py <markdown_file> <output_directory>
```

### Example

```bash
python markdown-code-extract.py example.md output/
```

This command will extract code blocks from `example.md` and save them in the `output/` directory.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sv4u/markdown-code-extract.git
    cd markdown-code-extract
    ```

2. Run the script using the following command:

    ```bash
    python markdown-code-extract.py <markdown_file> <output_directory>
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

For any inquiries, please contact [Sasank Vishnubhatla](mailto:svishnubhatla@cert.org).
