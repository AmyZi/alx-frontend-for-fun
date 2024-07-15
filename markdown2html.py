#!/usr/bin/env python3
import sys
import os
import re
import hashlib

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def process_line(line):
    # Convert headings
    heading_match = re.match(r'^(#{1,6}) (.*)', line)
    if heading_match:
        level = len(heading_match.group(1))
        heading_text = heading_match.group(2)
        return f"<h{level}>{heading_text}</h{level}>"

    # Convert unordered list items
    if line.startswith('- '):
        return f"<li>{process_inline_syntax(line[2:])}</li>"

    # Convert paragraphs and inline syntax
    return f"<p>{process_inline_syntax(line)}</p>"

def process_inline_syntax(text):
    # Convert bold syntax
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Convert italic syntax
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)

    # Convert MD5 syntax
    text = re.sub(r'\[\[(.*?)\]\]', lambda match: md5_hash(match.group(1)), text)

    # Remove 'c' characters (case insensitive)
    text = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), text)

    return text

def convert_markdown_to_html(markdown_content):
    html_content = ""
    lines = markdown_content.split('\n')
    in_list = False

    for line in lines:
        if line.startswith('- '):
            if not in_list:
                html_content += "<ul>\n"
                in_list = True
            html_content += process_line(line) + "\n"
        else:
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            if line.strip() != "":
                html_content += process_line(line) + "\n"
            else:
                html_content += "<br/>\n"

    if in_list:
        html_content += "</ul>\n"

    return html_content

def main():
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the Markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    sys.exit(0)

if __name__ == "__main__":
    main()
