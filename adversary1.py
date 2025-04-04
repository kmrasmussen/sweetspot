import random
import re

def adversary_toy1_function(problem):
    code = problem.python_solution
    # Find all non-whitespace characters and their positions
    non_whitespace_matches = list(re.finditer(r'\S', code))
    
    if not non_whitespace_matches:
        return code  # No non-whitespace characters to modify
    
    # Choose a random non-whitespace character
    chosen_match = random.choice(non_whitespace_matches)
    position = chosen_match.start()
    original_char = code[position]
    
    # Determine a replacement character that's different
    possible_replacements = {
        '(': ')',
        ')': '(',
        '[': ']',
        ']': '[',
        '{': '}',
        '}': '{',
        '+': '-',
        '-': '+',
        '*': '/',
        '/': '*',
        '=': '==',
        '==': '=',
        '>': '<',
        '<': '>',
        ',': ';',
        ';': ',',
        '.': ',',
        ':': ';',
        "'": '"',
        '"': "'",
        'True': 'False',
        'False': 'True',
        'and': 'or',
        'or': 'and'
    }
    
    # For single characters
    if len(original_char) == 1:
        if original_char in possible_replacements:
            replacement = possible_replacements[original_char]
        else:
            # For other characters, try to find a reasonable replacement
            if original_char.isalpha():
                # Replace with a different letter
                alphabet = 'abcdefghijklmnopqrstuvwxyz'
                replacement = random.choice(alphabet.replace(original_char.lower(), ''))
                if original_char.isupper():
                    replacement = replacement.upper()
            elif original_char.isdigit():
                # Replace with a different digit
                replacement = random.choice('0123456789'.replace(original_char, ''))
            else:
                # Replace with another special character
                replacement = random.choice('!@#$%^&*_+-=;:,./<>?')
    else:
        # For keywords that might be matched
        replacement = possible_replacements.get(original_char, 'x')
    
    # Create the buggy code by replacing the chosen character
    buggy_code = code[:position] + replacement + code[position + len(original_char):]
    return buggy_code

import ast
import random
import tokenize
from io import BytesIO
import token as token_module

def adversary_toy2_function(problem):
    print('INSIDE ADVERSARY-TOY2')
    code = problem.python_solution
    """
    Introduces a tiny bug in valid Python code while ensuring the result is still valid Python.
    
    Args:
        code (str): Valid Python code
    
    Returns:
        str: Python code with a tiny bug introduced
    """
    # First tokenize the code
    tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    
    # Filter for tokens we can safely modify
    modifiable_tokens = [
        (i, tok) for i, tok in enumerate(tokens) 
        if tok.type in (token_module.NAME, token_module.NUMBER, token_module.OP) 
        and tok.string.strip() and tok.type != token_module.ENCODING
    ]
    
    if not modifiable_tokens:
        return code  # No suitable tokens to modify
    
    # Choose a random token to modify
    idx, token = random.choice(modifiable_tokens)
    
    # Create a modified version based on token type
    modified_code = code
    if token.type == token_module.NAME:
        # Modify variable names, function names, etc.
        # We'll just change one character in the name
        if len(token.string) > 1:
            char_pos = random.randint(0, len(token.string) - 1)
            # Get the character range in the original string
            start_pos = token.start[1] + char_pos
            end_pos = start_pos + 1
            # Replace with a different letter while preserving case
            original_char = token.string[char_pos]
            if original_char.isalpha():
                replacement = random.choice('abcdefghijklmnopqrstuvwxyz'.replace(original_char.lower(), ''))
                if original_char.isupper():
                    replacement = replacement.upper()
                modified_code = code[:start_pos] + replacement + code[end_pos:]
    
    elif token.type == token_module.NUMBER:
        # Modify numeric literals slightly
        if '.' in token.string:  # Float
            num = float(token.string)
            modified_num = num + random.choice([-0.1, 0.1])
            modified_code = code[:token.start[1]] + str(modified_num) + code[token.end[1]:]
        else:  # Integer
            num = int(token.string)
            modified_num = num + random.choice([-1, 1])
            modified_code = code[:token.start[1]] + str(modified_num) + code[token.end[1]:]
    
    elif token.type == token_module.OP:
        # Modify operators
        op_replacements = {
            '+': '-', '-': '+', '*': '/', '/': '*',
            '<': '>', '>': '<', '==': '!=', '!=': '==',
            '<=': '>=', '>=': '<=', 'and': 'or', 'or': 'and'
        }
        if token.string in op_replacements:
            replacement = op_replacements[token.string]
            modified_code = code[:token.start[1]] + replacement + code[token.end[1]:]
    
    
    return modified_code

import ast
import random
import tokenize
from io import BytesIO
import token as token_module

def adversary_toy3_function(problem):
    intensity = 3
    code = problem.python_solution
    """
    Introduces bugs in valid Python code while ensuring the result is still valid Python.
    
    Args:
        code (str): Valid Python code
        intensity (int): Number of bugs to introduce (defaults to 1)
    
    Returns:
        str: Python code with bugs introduced
    """
    # Start with original code
    modified_code = code
    
    # Track number of successful modifications
    successful_mods = 0
    max_attempts = intensity * 3  # Allow some failed attempts
    attempts = 0
    
    while successful_mods < intensity and attempts < max_attempts:
        attempts += 1
        
        # Tokenize the current version of the code
        try:
            tokens = list(tokenize.tokenize(BytesIO(modified_code.encode('utf-8')).readline))
        except:
            continue  # If tokenizing fails, try again
            
        # Filter for tokens we can safely modify
        modifiable_tokens = [
            (i, tok) for i, tok in enumerate(tokens) 
            if tok.type in (token_module.NAME, token_module.NUMBER, token_module.OP) 
            and tok.string.strip() and tok.type != token_module.ENCODING
        ]
        
        if not modifiable_tokens:
            break  # No suitable tokens to modify
        
        # Choose a random token to modify
        idx, token = random.choice(modifiable_tokens)
        
        # Create a candidate modified version
        candidate_code = modified_code
        token_modified = False
        
        if token.type == token_module.NAME:
            # Modify variable names, function names, etc.
            if len(token.string) > 1 and token.string not in ('def', 'if', 'for', 'while', 'import', 'class', 'return', 'True', 'False', 'None'):
                char_pos = random.randint(0, len(token.string) - 1)
                start_pos = token.start[1] + char_pos
                end_pos = start_pos + 1
                original_char = token.string[char_pos]
                if original_char.isalpha():
                    replacement = random.choice('abcdefghijklmnopqrstuvwxyz'.replace(original_char.lower(), ''))
                    if original_char.isupper():
                        replacement = replacement.upper()
                    candidate_code = modified_code[:start_pos] + replacement + modified_code[end_pos:]
                    token_modified = True
        
        elif token.type == token_module.NUMBER:
            # Modify numeric literals slightly
            try:
                if '.' in token.string:  # Float
                    num = float(token.string)
                    modified_num = num + random.choice([-0.1, 0.1])
                    candidate_code = modified_code[:token.start[1]] + str(modified_num) + modified_code[token.end[1]:]
                    token_modified = True
                else:  # Integer
                    num = int(token.string)
                    modified_num = num + random.choice([-1, 1])
                    candidate_code = modified_code[:token.start[1]] + str(modified_num) + modified_code[token.end[1]:]
                    token_modified = True
            except ValueError:
                pass  # Skip if we can't convert to number
        
        elif token.type == token_module.OP:
            # Modify operators
            op_replacements = {
                '+': '-', '-': '+', '*': '/', '/': '*', '//': '/',
                '<': '>', '>': '<', '==': '!=', '!=': '==',
                '<=': '>=', '>=': '<=', 'is': 'is not', 'is not': 'is',
                'in': 'not in', 'not in': 'in'
            }
            if token.string in op_replacements:
                replacement = op_replacements[token.string]
                candidate_code = modified_code[:token.start[1]] + replacement + modified_code[token.end[1]:]
                token_modified = True
        
        # Verify the modified code is still valid Python
        if token_modified:
            try:
                ast.parse(candidate_code)
                modified_code = candidate_code
                successful_mods += 1
            except SyntaxError:
                continue  # If invalid, ignore this modification and try again
    
    return modified_code