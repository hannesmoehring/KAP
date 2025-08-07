import argparse
import datetime as dt

import src.testing_kap.test_util as test_util


def main():
    parser = argparse.ArgumentParser(description="Path to CSV file")
    parser.add_argument("-p", "--path_to_csv", type=str, nargs="?", default=None, help="Path to the CSV file (optional)")
    args = parser.parse_args()

    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M")
    if args.path_to_csv:
        print(f"Using CSV file at {args.path_to_csv} to create config.")
        test_util.generate_config_from_csv(args.path_to_csv, f"config_{timestamp}.json")


if __name__ == "__main__":
    main()
