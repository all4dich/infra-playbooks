import csv
import argparse
import logging

# Set logging level
logging.getLogger().setLevel(logging.INFO)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--csv_file", help="CSV file to read", default="/Users/sunjoo/work/nota-github/infra-playbooks/data/nota-gpu-assign-table.csv")
args = arg_parser.parse_args()

if __name__ == "__main__":
    # Read csv file  and create a dictionary with key as hostname and value as gpu id

    csv_file = args.csv_file
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        gpu_assign_list = list(reader)

    # Convert the list to a dictionary
    gpu_assign_dict = {}
    for row in gpu_assign_list:
        gpu_assign_dict[row['Host'] + '-' + row['GPU_id']] = row
    logging.info("Done")


