import re

def convert_markdown_to_html(md_text):
    html_lines = []

    for line in md_text.split('\n'):
        line = line.strip()

        # Heading
        if line.startswith("#"):
            hashes = len(line) - len(line.lstrip('#'))
            content = line.lstrip('#').strip()
            html_lines.append(f"<h{hashes}>{content}</h{hashes}>")

        # List item
        elif line.startswith("- "):
            content = line[2:].strip()
            # Bold
            content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
            # Italic
            content = re.sub(r"\*(.+?)\*", r"<em>\1</em>", content)
            # Link
            content = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href='\2'>\1</a>", content)
            html_lines.append(f"<li>{content}</li>")

        # Paragraph (normal line)
        elif line:
            line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)  # Bold
            line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)              # Italic
            line = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href='\2'>\1</a>", line)  # Link
            html_lines.append(f"<p>{line}</p>")

    # Wrap <li> inside <ul>
    final_html = []
    in_list = False
    for line in html_lines:
        if line.startswith("<li>") and not in_list:
            final_html.append("<ul>")
            in_list = True
        elif not line.startswith("<li>") and in_list:
            final_html.append("</ul>")
            in_list = False
        final_html.append(line)
    if in_list:
        final_html.append("</ul>")

    return "\n".join(final_html)
