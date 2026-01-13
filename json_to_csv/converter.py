import sys
from pathlib import Path
import json

def convert(input, output):
    with open(input, "r") as file:
        content = json.load(file)

    info = list(content[0].keys())
    
    with open(output, "wt") as f:
        f.write(",".join(info) + "\n")
        for person in content:
            values = []
            for key in info:
                values.append(str(person[key]))
            f.write(",".join(values) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("To run this converter, you need to provide 2 arguments, the input file name and the output file name")

    input = sys.argv[1]
    output = sys.argv[2]

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if input_path.suffix.lower() != ".json":
        print(f"Error: '{input_path.name}' is not a JSON file.")
        sys.exit(1)

    if output_path.suffix.lower() != ".csv":
        print(f"Error: 'f{output_path.name}' is not a CSV file.")
        sys.exit(1)

    if not input_path.exists():
        print(f"Error: The file {input_path} was not found")
        sys.exit(1)

    convert(input, output)
    