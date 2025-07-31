# This is the main entrypoint for the program.
import src.config

import src.testing_kap.test_util as test_util

def main():
    df = test_util.routine()
    
    config = src.config.Config("./config.json")

    parsers = config.get_parsers()
    checks = config.get_checks()

    for parser in parsers:
        parser.parse_columns(df)

    for check in checks:
        r = check.run_check(df)
        print(r)

if __name__ == "__main__":
    main()