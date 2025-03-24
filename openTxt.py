def openTxt(filePath):
    text = ""  # Initialize text with a default value
    try:
        with open(filePath, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    
    return text
