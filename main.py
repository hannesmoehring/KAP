# This is the main entrypoint for the program.
import src.config

import src.testing_kap.test_util as test_util

def main():

    config = src.config.Config("./config.json")
    checks = config.get_checks()

    df = test_util.routine()

    for check in checks:
        r = check.run_check(df)

        print(r)


if __name__ == "__main__":
    main()