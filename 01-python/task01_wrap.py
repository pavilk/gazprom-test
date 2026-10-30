width = 70

def wrap_text(text: str) -> str:
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            if not current:
                current = word
            elif len(current) + 1 + len(word) <= width:
                current += " " + word
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return "\n".join(lines)
