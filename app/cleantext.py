import re
import spacy
nlp = spacy.load("en_core_web_md")


def clean_doc(text):
    punct_regex = r"[^0-9a-zA-Z\s]"
    special_chars_regex = r"[\$\%\&\@+]"
    whitespace_regex = r"\s+"
    newline_regex = r"\n+"

    text = re.sub(punct_regex, "", text)
    text = re.sub(special_chars_regex, "", text)
    text = re.sub(whitespace_regex, " ", text)
    text = re.sub(newline_regex, " ", text)

    text = text.lower().strip()
    return text


def tokenizer(text):
    tokens = []
    for token in nlp(text):
        if (not token.is_punct) & (not token.is_space):
            tokens.append(token.text.lower())
    return tokens
