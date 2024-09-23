

def write_to_markdown(filepath, content):
    """Write content to a markdown file."""
    with open(filepath, 'w') as file:
        file.write(content)

def format_section(title, body):
    """Format a markdown section."""
    return f"## {title}\n\n{body}\n\n"