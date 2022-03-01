import re

def clean_doc(text):
  punct_regex = r"[^0-9a-zA-Z\s]" # any non-alphanumeric chars
  special_chars_regex = r"[\$\%\&\@+]" 
  whitespace_regex = r"\s+"
  newline_regex = r"\n+"

  text = re.sub(punct_regex, "", text)
  text = re.sub(special_chars_regex, "", text)
  text = re.sub(whitespace_regex, " ", text)
  text = re.sub(newline_regex, " ", text)

  # case normalize and strip extra white spaces on the far left and right hand side
  text = text.lower().strip()
  return text