import easyocr

reader = easyocr.Reader(['en'])  # English for now


def extract_text(image_path):
    results = reader.readtext(image_path)
    lines = [text for (bbox, text, conf) in results]
    return "\n".join(lines)