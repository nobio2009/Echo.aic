def split_command(text, start_index=2):
    words = text.split()
    return " ".join(words[start_index:])
