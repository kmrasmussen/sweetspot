import re

def remove_comments(source_code):
    # Remove comments but preserve newlines
    return re.sub(r'#.*?(\n|$)', r'\1', source_code)

if __name__ == "__main__":
  some_commented_code = """
  a, b = map(int, input().split())
  c, s = a, 0
  while a >= b:
      s += (a // b) + 1  # Introduced a bug by adding 1 to the new candles count
      a = (a // b) + (a % b)
  print(s + c)
  """
  print('commentremoved code:')
  print(remove_comments(some_commented_code))