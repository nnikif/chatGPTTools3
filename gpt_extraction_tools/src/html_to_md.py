import html2text
import argparse

def extract_md_from_html(html_content):
    """
    Extracts Markdown from HTML content.

    Args:
        html_content (str): The HTML content to convert.

    Returns:
        str: The converted Markdown content.
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = False
    h.ignore_tables = False
    h.ignore_mailto_links = True
    return h.handle(html_content)

def main():
    parser = argparse.ArgumentParser(description="Convert HTML file to Markdown.")
    parser.add_argument("input_file", help="Path to the input HTML file")
    parser.add_argument("-o", "--output_file", help="Path to the output Markdown file", default=None)
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    markdown_content = extract_md_from_html(html_content)

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)
    else:
        print(markdown_content)

if __name__ == "__main__":
    main()