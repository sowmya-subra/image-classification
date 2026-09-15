import numpy as np


class BadCSV(Exception):
    """Raised when an uploaded file can't be turned into a 28x28 image."""


def parse_csv(uploaded_file):
    try:
        text = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        raise BadCSV("That doesn't look like a text file. Please upload a CSV.")

    rows = [line for line in text.strip().splitlines() if line.strip()]
    values = []
    for line in rows:
        for cell in line.split(","):
            try:
                values.append(float(cell))
            except ValueError:
                raise BadCSV("The file contains something that isn't a number.")

    if len(values) != 784:
        raise BadCSV(
            f"Expected 784 pixel values (28x28), but found {len(values)}."
        )

    array = np.array(values, dtype="float32")

    if array.max() > 1.0:
        array = array / 255.0

    return array.reshape(1, 28, 28, 1)