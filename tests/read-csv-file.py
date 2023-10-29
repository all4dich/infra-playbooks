import csv
import argparse
import logging

# Set logging level
logging.getLogger().setLevel(logging.INFO)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--csv_file", help="CSV file to read", default="/Users/sunjoo/work/nota-github/infra-playbooks/data/nota-gpu-assign-table.csv")

if __name__ == "__main__":
    # Read csv file  and create a list of dictionary
    args = arg_parser.parse_args()
    csv_file = args.csv_file
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        gpu_assign_list = list(reader)
        logging.info(f"gpu_assign_list = {gpu_assign_list}")
