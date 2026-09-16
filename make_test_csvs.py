import csv
import os
import numpy as np


OUTPUT_DIR = "sample_csvs"


def write_csv(filename, data):
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Valid CSV files
# -----------------------------

# Valid 28x28 image using 0-255 values
valid_255 = np.random.randint(0, 256, size=(28, 28))

write_csv(
    "valid_0_to_255.csv",
    valid_255
)


# Valid 28x28 image using 0-1 values
valid_01 = np.random.rand(28, 28)

write_csv(
    "valid_0_to_1.csv",
    valid_01
)


# -----------------------------
# Invalid CSV files
# -----------------------------

# 27 rows instead of 28
bad_27_rows = np.zeros((27, 28))

write_csv(
    "bad_27_rows.csv",
    bad_27_rows
)


# One row has only 27 columns
bad_ragged = np.zeros((28, 28)).tolist()
bad_ragged[5] = [0] * 27

write_csv(
    "bad_ragged_row.csv",
    bad_ragged
)


# 784 values in one row instead of 28x28
bad_flattened = np.zeros((1, 784))

write_csv(
    "bad_flattened_784.csv",
    bad_flattened
)


# Negative value
bad_negative = np.zeros((28, 28))
bad_negative[10, 10] = -1

write_csv(
    "bad_negative_value.csv",
    bad_negative
)


# Value greater than 255
bad_too_large = np.zeros((28, 28))
bad_too_large[10, 10] = 256

write_csv(
    "bad_out_of_range.csv",
    bad_too_large
)


# Non-numeric value
bad_non_numeric = np.zeros((28, 28), dtype=object)
bad_non_numeric[10, 10] = "hello"

write_csv(
    "bad_non_numeric.csv",
    bad_non_numeric
)


# Header
header_data = [["pixel"] * 28] + np.zeros((28, 28)).tolist()

write_csv(
    "bad_has_header.csv",
    header_data
)


# Empty CSV
open(
    os.path.join(OUTPUT_DIR, "bad_empty.csv"),
    "w"
).close()


# Not actually a CSV
with open(
    os.path.join(OUTPUT_DIR, "bad_not_a_csv.txt"),
    "w"
) as f:
    f.write("This is not a CSV file.")


print("Test CSV files created in:", OUTPUT_DIR)