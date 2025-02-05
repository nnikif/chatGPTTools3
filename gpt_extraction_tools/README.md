```markdown
# GPT Extraction Tools

This project provides tools for extracting and processing HTML content, specifically focusing on user and assistant messages. The tools include functionality for filtering HTML content, converting HTML to Markdown, and saving user and assistant message pairs to separate files.

## Features

- Filter HTML content to include only user and assistant messages.
- Insert custom content before user and assistant messages.
- Replace specific HTML tags with custom content.
- Save user and assistant message pairs to separate HTML files.
- Optionally add Markdown versions of the pairs.
- Numbering options for file names and content, including decimal and Roman numeral formats.

## Requirements

- Python 3.x
- `beautifulsoup4`
- `html2text`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/nnikif/chatGPTTools3.git
    cd chatGPTTools3
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Interface

The main script `filter_html.py` provides a command-line interface for processing HTML files.

```bash
python filter_html.py [options] input_file
```

### Options

- `-o`, `--output_file`: Path to the output HTML file.
- `--skip-user`: Skip elements with `data-message-author-role="user"`.
- `--q-file`: Path to the `q.html` file to insert before user messages.
- `--a-file`: Path to the `a.html` file to insert before assistant messages.
- `--divider-file`: Path to the `divider.html` file to replace specific HTML tags.
- `--output-json`: Path to the output JSON file for user & assistant tuples.
- `--output-folder`: Path to the folder to save user & assistant pairs as separate HTML files.
- `--add-markdown`: Add Markdown versions of the pairs to the output folder.
- `--number-base`: Base number for numbering (0 or 1).
- `--number-format`: Format of the number (`decimal` or `roman`).

### Example

```bash
python filter_html.py --q-file path/to/q.html --a-file path/to/a.html --divider-file path/to/divider.html --output-folder path/to/output_folder --add-markdown --number-base 1 --number-format roman input.html
```