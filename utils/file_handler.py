def read_sales_data(filename):
    """
    Reads sales data handling encoding issues
    Returns list of raw lines
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()
                break

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print("File not found")
            return []

    else:
        print("Unable to decode file")
        return []

    # remove header + empty lines
    cleaned = []
    for line in lines[1:]:
        line = line.strip()
        if line:
            cleaned.append(line)

    return cleaned
