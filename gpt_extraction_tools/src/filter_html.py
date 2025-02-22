from bs4 import BeautifulSoup
import argparse
import json
import os
import html2text

def filter_html_by_role(html_content, skip_user=False, q_content=None, a_content=None):
    """
    Filters HTML content to include only elements with data-message-author-role="user" or "assistant",
    and inserts q_content before "user" elements and a_content before "assistant" elements.

    Args:
        html_content (str): The HTML content to filter.
        skip_user (bool): Whether to skip elements with data-message-author-role="user".
        q_content (str): Content to insert before "user" elements.
        a_content (str): Content to insert before "assistant" elements.

    Returns:
        str: The filtered and modified HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    roles = ["assistant"] if skip_user else ["user", "assistant"]
    filtered_elements = soup.find_all(attrs={"data-message-author-role": roles})
    
    filtered_html = ''
    for element in filtered_elements:
        if element['data-message-author-role'] == 'user' and q_content:
            filtered_html += q_content
        elif element['data-message-author-role'] == 'assistant' and a_content:
            filtered_html += a_content
        filtered_html += str(element)
    
    return filtered_html

def extract_user_assistant_pairs(html_content, skip_user=False):
    """
    Extracts pairs of user and assistant messages from HTML content.

    Args:
        html_content (str): The HTML content to process.
        skip_user (bool): Whether to skip elements with data-message-author-role="user".

    Returns:
        list: A list of tuples, each containing a user message and an assistant message.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    user_messages = soup.find_all(attrs={"data-message-author-role": "user"})
    assistant_messages = soup.find_all(attrs={"data-message-author-role": "assistant"})
    
    pairs = []
    if skip_user:
        for assistant in assistant_messages:
            pairs.append(("", str(assistant)))
    else:
        for user, assistant in zip(user_messages, assistant_messages):
            pairs.append((str(user), str(assistant)))
    
    return pairs

def replace_spans_with_divider(html_content, divider_content):
    """
    Replaces all <span class="" data-state="closed"> tags in the HTML content with the provided divider content.

    Args:
        html_content (str): The HTML content to modify.
        divider_content (str): The content to replace <span> tags with.

    Returns:
        str: The modified HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for span in soup.find_all('span', attrs={"data-state": "closed"}):
        span.replace_with(BeautifulSoup(divider_content, 'html.parser'))
    return str(soup)

def int_to_roman(num):
    """
    Converts an integer to a Roman numeral.

    Args:
        num (int): The integer to convert.

    Returns:
        str: The Roman numeral representation of the integer.
    """
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def save_pairs_to_folder(pairs, folder_name, q_content=None, a_content=None, divider_content=None, add_markdown=False, number_base=0, number_format="decimal"):
    """
    Saves user and assistant message pairs to separate HTML files in the specified folder,
    including q_content before user messages and a_content before assistant messages,
    and replacing <span class="" data-state="closed"> tags with divider_content.
    Optionally adds Markdown versions of the pairs.

    Args:
        pairs (list): A list of tuples, each containing a user message and an assistant message.
        folder_name (str): The name of the folder to save the files in.
        q_content (str): Content to insert before user messages.
        a_content (str): Content to insert before assistant messages.
        divider_content (str): Content to replace <span> tags with.
        add_markdown (bool): Whether to add Markdown versions of the pairs.
        number_base (int): Base number for numbering (0 or 1).
        number_format (str): Format of the number ("decimal" or "roman").
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for i, (user_message, assistant_message) in enumerate(pairs):
        file_number = f"{i:03}"
        actual_number = i + number_base
        if number_format == "roman":
            actual_number = int_to_roman(actual_number)
        else:
            actual_number = str(actual_number)
        current_divider_content = divider_content.replace("{number_length}", actual_number)
        current_q_content = q_content.replace("{number_length}", actual_number) if q_content else ''
        current_a_content = a_content.replace("{number_length}", actual_number) if a_content else ''
        
        file_name = os.path.join(folder_name, f"{file_number}.html")
        with open(file_name, "w", encoding="utf-8") as file:
            if user_message and current_q_content:
                file.write(f"{current_q_content}\n")
            if user_message:
                user_message = replace_spans_with_divider(user_message, current_divider_content)
                file.write(f"{user_message}\n")
            if assistant_message and current_a_content:
                file.write(f"{current_a_content}\n")
            if assistant_message:
                assistant_message = replace_spans_with_divider(assistant_message, current_divider_content)
                file.write(f"{assistant_message}\n")
        
        if add_markdown:
            markdown_file_name = os.path.join(folder_name, f"{file_number}.md")
            with open(markdown_file_name, "w", encoding="utf-8") as md_file:
                h = html2text.HTML2Text()
                h.ignore_links = True
                h.ignore_images = True
                h.ignore_emphasis = False
                h.ignore_tables = False
                h.ignore_mailto_links = True
                if user_message:
                    md_file.write(h.handle(user_message))
                if assistant_message:
                    md_file.write(h.handle(assistant_message))

def main():
    parser = argparse.ArgumentParser(description="Filter HTML file to include only user and assistant messages.")
    parser.add_argument("input_file", help="Path to the input HTML file")
    parser.add_argument("-o", "--output_file", help="Path to the output HTML file", default=None)
    parser.add_argument("--skip-user", action="store_true", help="Skip elements with data-message-author-role='user'")
    parser.add_argument("--q-file", help="Path to the q.html file", default=None)
    parser.add_argument("--a-file", help="Path to the a.html file", default=None)
    parser.add_argument("--divider-file", help="Path to the divider.html file", default=None)
    parser.add_argument("--output-json", help="Path to the output JSON file for user & assistant tuples", default=None)
    parser.add_argument("--output-folder", help="Path to the folder to save user & assistant pairs as separate HTML files", default=None)
    parser.add_argument("--add-markdown", action="store_true", help="Add Markdown versions of the pairs to the output folder")
    parser.add_argument("--number-base", type=int, choices=[0, 1], default=0, help="Base number for numbering (0 or 1)")
    parser.add_argument("--number-format", choices=["decimal", "roman"], default="decimal", help="Format of the number (decimal or roman)")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    q_content = ''
    a_content = ''
    divider_content = ''
    if args.q_file:
        with open(args.q_file, "r", encoding="utf-8") as file:
            q_content = file.read()
    if args.a_file:
        with open(args.a_file, "r", encoding="utf-8") as file:
            a_content = file.read()
    if args.divider_file:
        with open(args.divider_file, "r", encoding="utf-8") as file:
            divider_content = file.read()

    filtered_html = filter_html_by_role(html_content, skip_user=args.skip_user, q_content=q_content, a_content=a_content)
    filtered_html = replace_spans_with_divider(filtered_html, divider_content.replace("{number_length}", ""))

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as file:
            file.write(filtered_html)
    else:
        print(filtered_html)

    user_assistant_pairs = extract_user_assistant_pairs(html_content, skip_user=args.skip_user)

    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as file:
            json.dump(user_assistant_pairs, file, ensure_ascii=False, indent=4)

    if args.output_folder:
        save_pairs_to_folder(user_assistant_pairs, args.output_folder, q_content=q_content, a_content=a_content, divider_content=divider_content, add_markdown=args.add_markdown, number_base=args.number_base, number_format=args.number_format)

if __name__ == "__main__":
    main()