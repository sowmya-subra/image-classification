import os

from classifier.csv_parser import parse_csv, BadCSV


TEST_FOLDER = "sample_csvs"


for filename in sorted(os.listdir(TEST_FOLDER)):

    path = os.path.join(TEST_FOLDER, filename)

    print(f"\nTesting: {filename}")

    try:

        with open(path, "rb") as f:
            result = parse_csv(f)

        print("  ACCEPTED")
        print("  Shape:", result.shape)
        print("  Type:", result.dtype)
        print("  Min:", result.min())
        print("  Max:", result.max())

    except BadCSV as e:

        print("  REJECTED")
        print(" ", e)