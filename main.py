# This is the main entrypoint for the program.
import argparse

import pandas as pd

import argparse

import pandas as pd

import src.config
import src.testing_kap.test_util as test_util
from src.checks.check import Check
from src.types import GenericResponse, Result


def main():
    parser = argparse.ArgumentParser(description="Path to CSV file")
    parser.add_argument("path_to_csv", type=str, nargs="?", default=None, help="Path to the CSV file (optional)")
    args = parser.parse_args()
    if not args.path_to_csv:
        df = test_util.routine()
        print("No path to CSV file provided. Using test data.")
    else:
        print(f"Using CSV file at {args.path_to_csv}.")
        df = pd.read_csv(args.path_to_csv)

    num_rows = df.shape[0]

    config = src.config.Config("./config.json")

    parsers = config.get_parsers()

    stage_1_checks = config.get_stage_1_checks()
    stage_2_checks = config.get_stage_2_checks()
    stage_3_checks = config.get_stage_3_checks()

    stage_1_checks = config.get_stage_1_checks()
    stage_2_checks = config.get_stage_2_checks()
    stage_3_checks = config.get_stage_3_checks()

    for parser in parsers:
        parser.parse_columns(df)

    results_stage_1: list[GenericResponse] = []
    results_stage_2: list[GenericResponse] = []
    results_stage_3: list[GenericResponse] = []

    bad_id_set = set()
    failed_checks: list[Check] = []
    count_failed_stage_1: int = 0
    count_failed_stage_2: int = 0
    count_failed_stage_3: int = 0
    count: int = 0
    print("------------------------- NOW EXECUTING STAGE 1 CHECKS -------------------------")
    for check in stage_1_checks:
        count += 1
        try:
            r = check.run_check(df)
        except Exception as e:
            # r.failed = True
            print(f"Error occured while running check {check}: {e}")
            failed_checks.append(check)
            count_failed_stage_1 += 1
            continue  # todo : should be bad id?

        results_stage_1.append(r)
        bad_id_set.update(r.bad_id_list)
    print(f"Executed {count} stage 1 checks.")
    count = 0
    print("------------------------- NOW EXECUTING STAGE 2 CHECKS -------------------------")
    for check in stage_2_checks:
        count += 1
        try:
            r = check.run_check(df)
        except Exception as e:
            # r.failed = True
            print(f"Error occured while running check {check}: {e}")
            failed_checks.append(check)
            count_failed_stage_2 += 1
            continue
        results_stage_2.append(r)
        bad_id_set.update(r.bad_id_list)
    print(f"Executed {count} stage 2 checks.")
    count = 0
    print("------------------------- NOW EXECUTING STAGE 3 CHECKS -------------------------")
    for check in stage_3_checks:
        count += 1
        try:
            r = check.run_check(df)
        except Exception:
            # r.failed = True
            failed_checks.append(check)
            count_failed_stage_3 += 1
            continue  # todo : should be bad id?
        results_stage_3.append(r)
        bad_id_set.update(r.bad_id_list)
    print(f"Executed {count} stage 3 checks.")
    count = 0
    print("------------------------- ALL CHECKS COMPLETED -------------------------")
    print(f"Total number of checks: {len(stage_1_checks) + len(stage_2_checks) + len(stage_3_checks)}")
    if len(failed_checks) > 0:
        print(f"Total number of failed checks: \033[91m{len(failed_checks)}\033[0m")
    else:
        print("All checks ran successfully. No failed checks.")
    print("\n")
    print(f"Results Stage 1: {len(stage_1_checks) - count_failed_stage_1}/{len(stage_1_checks)} checks executed")
    print(f"Results Stage 2: {len(stage_2_checks) - count_failed_stage_2}/{len(stage_2_checks)} checks executed")
    print(f"Results Stage 3: {len(stage_3_checks) - count_failed_stage_3}/{len(stage_3_checks)} checks executed")
    print("\n")
    print(f"Total number of rows in the DataFrame: {num_rows}")
    print(f"Total number of bad IDs: \033[91m{len(bad_id_set)}\033[0m")
    print(f"Score: {num_rows - len(bad_id_set)} / {num_rows} -> {round((num_rows - len(bad_id_set)) / num_rows * 100, 2)}%")
    print("\n")

    print("------------------------- EXPORTING RESULTS -------------------------")
    results = Result(
        results_stage_1=results_stage_1,
        results_stage_2=results_stage_2,
        results_stage_3=results_stage_3,
        count_failed_stage_1=count_failed_stage_1,
        count_failed_stage_2=count_failed_stage_2,
        count_failed_stage_3=count_failed_stage_3,
        bad_id_set=bad_id_set,
    )
    test_util.export_to_json(results)
    print("------------------------- RESULTS EXPORT COMPLETED -------------------------")


if __name__ == "__main__":
    main()
