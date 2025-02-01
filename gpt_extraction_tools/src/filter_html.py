from bs4 import BeautifulSoup
import argparse
import json

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

def extract_user_assistant_pairs(html_content):
    """
    Extracts pairs of user and assistant messages from HTML content.

    Args:
        html_content (str): The HTML content to process.

    Returns:
        list: A list of tuples, each containing a user message and an assistant message.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    user_messages = soup.find_all(attrs={"data-message-author-role": "user"})
    assistant_messages = soup.find_all(attrs={"data-message-author-role": "assistant"})
    
    pairs = []
    for user, assistant in zip(user_messages, assistant_messages):
        pairs.append((user.get_text(strip=True), assistant.get_text(strip=True)))
    
    return pairs

def main():
    parser = argparse.ArgumentParser(description="Filter HTML file to include only user and assistant messages.")
    parser.add_argument("input_file", help="Path to the input HTML file")
    parser.add_argument("-o", "--output_file", help="Path to the output HTML file", default=None)
    parser.add_argument("--skip-user", action="store_true", help="Skip elements with data-message-author-role='user'")
    parser.add_argument("--q-file", help="Path to the q.html file", default=None)
    parser.add_argument("--a-file", help="Path to the a.html file", default=None)
    parser.add_argument("--output-json", help="Path to the output JSON file for user & assistant tuples", default=None)
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    q_content = ''
    a_content = ''
    if args.q_file:
        with open(args.q_file, "r", encoding="utf-8") as file:
            q_content = file.read()
    if args.a_file:
        with open(args.a_file, "r", encoding="utf-8") as file:
            a_content = file.read()

    filtered_html = filter_html_by_role(html_content, skip_user=args.skip_user, q_content=q_content, a_content=a_content)

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as file:
            file.write(filtered_html)
    else:
        print(filtered_html)

    if args.output_json:
        user_assistant_pairs = extract_user_assistant_pairs(html_content)
        with open(args.output_json, "w", encoding="utf-8") as file:
            json.dump(user_assistant_pairs, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()