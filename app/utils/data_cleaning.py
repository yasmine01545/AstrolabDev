import re


def clean_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r"```(?:text|markdown|html|french|arabic|english|[a-zA-Z]+)?\n*|\n*```", "", text).strip()
    text = re.sub(r"^(Okay,.*?\n\n)", "", text, flags=re.MULTILINE)
    text = re.sub(r"[\*\#]+|\[.*?\]|\{.*?\}|^\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n([^\n-])", r"\n\n\1", text, flags=re.MULTILINE)
    return text.strip() 

