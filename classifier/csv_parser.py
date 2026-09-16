import csv
import io
import numpy as np


EXPECTED_SHAPE = (28, 28)
MAX_UPLOAD_BYTES = 1_000_000


class BadCSV(Exception):
    """Raised when an uploaded file can't be turned into a 28x28 image."""


def parse_csv(uploaded_file):
    """
    Validate and process an uploaded MNIST CSV.

    Returns:
        NumPy array with shape (1, 28, 28, 1), dtype float32,
        with pixel values scaled to the range 0-1.

    Raises:
        BadCSV: if the uploaded file is invalid.
    """

    # Check that a file was uploaded
    if uploaded_file is None:
        raise BadCSV("Please select a CSV file to upload.")

    # Check file extension
    filename = getattr(uploaded_file, "name", "")

    if not filename.lower().endswith(".csv"):
        raise BadCSV("Please upload a file with a .csv extension.")

    # Read the uploaded file
    try:
        uploaded_file.seek(0)
        raw = uploaded_file.read()
    except Exception:
        raise BadCSV("The uploaded file could not be read.")

    # Check for empty file
    if not raw:
        raise BadCSV("The uploaded CSV file is empty.")

    # Check file size
    if len(raw) > MAX_UPLOAD_BYTES:
        raise BadCSV(
            "The uploaded file is too large. "
            "Please upload a 28x28 CSV."
        )

    # Decode the file
    try:
        if isinstance(raw, bytes):
            text = raw.decode("utf-8-sig")
        else:
            text = raw
    except UnicodeDecodeError:
        raise BadCSV(
            "That doesn't look like a text file. "
            "Please upload a readable CSV."
        )

    # Parse CSV
    try:
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
    except csv.Error:
        raise BadCSV("The uploaded file is not a valid CSV.")

    # Remove completely blank rows
    rows = [
        row for row in rows
        if any(cell.strip() for cell in row)
    ]

    # Check for empty CSV
    if not rows:
        raise BadCSV("The uploaded CSV file is empty.")

    # Check number of rows
    if len(rows) != 28:
        raise BadCSV(
            f"The CSV must have exactly 28 rows and 28 columns. "
            f"Your file has {len(rows)} rows."
        )

    # Check number of columns in every row
    for row_number, row in enumerate(rows, start=1):
        if len(row) != 28:
            raise BadCSV(
                f"Row {row_number} has {len(row)} values. "
                "Every row must contain exactly 28 values."
            )

    # Convert values to numbers
    try:
        values = np.array(rows, dtype=np.float32)
    except (ValueError, TypeError):
        raise BadCSV(
            "Every value in the CSV must be a numeric pixel intensity."
        )

    # Check for NaN or infinity
    if not np.isfinite(values).all():
        raise BadCSV(
            "The CSV contains invalid values. "
            "Every pixel must be a finite number."
        )

    minimum = float(values.min())
    maximum = float(values.max())

    # Check for negative values
    if minimum < 0:
        raise BadCSV(
            "Pixel values cannot be negative. "
            "Use values between 0 and 255 or between 0 and 1."
        )

    # Check upper limit
    if maximum > 255:
        raise BadCSV(
            "Pixel values cannot be greater than 255."
        )

    # Detect 0-255 data and normalize to 0-1
    if maximum > 1:
        values = values / 255.0

    # Keep all values in the 0-1 range
    values = np.clip(values, 0.0, 1.0)

    # Reshape for the CNN
    values = values.reshape(1, 28, 28, 1)

    return values.astype(np.float32)
    