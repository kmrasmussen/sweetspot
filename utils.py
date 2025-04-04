import ast
from removecomments import remove_comments

def is_valid_python(code_string):
    try:
        ast.parse(code_string)
        return True
    except SyntaxError:
        return False
        
def extract_markdown_code(text):
    """
    Extract code from a markdown code block, assuming there's only one code block.
    Works even if there's text before and after the markdown block.
    
    Args:
        text (str): Text that contains a markdown code block
        
    Returns:
        str: The extracted code without the markdown delimiters
    """
    # Find the start and end of the code block
    start_marker = "```python"
    end_marker = "```"
    
    start_idx = text.find(start_marker)
    if start_idx == -1:
        # Try alternate marker without language specification
        start_marker = "```"
        start_idx = text.find(start_marker)
        if start_idx == -1:
            raise ValueError("No code block found in the text")
    
    # Move past the start marker
    start_idx += len(start_marker)
    
    # Find the end marker after the start marker
    end_idx = text.find(end_marker, start_idx)
    if end_idx == -1:
        raise ValueError("No closing code block marker found")
    
    # Extract the code between the markers
    code = text[start_idx:end_idx].strip()
    
    return remove_comments(code)

