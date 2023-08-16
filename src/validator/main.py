"""
This script loads a given CSV into a Pandas DataFrame, and then validates it against
the SBL Pandera schema.

Run from the terminal to see the generated output.
"""

import sys

import pandas as pd
from pandera.errors import SchemaErrors
from schema import get_schema_for_lei


def csv_to_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, na_filter=False)


def run_validation_on_df(df: pd.DataFrame, lei: str) -> None:
    """
    Run validaition on the supplied dataframe and print a report to
    the terminal.
    """

    print("--------------------------------------------------------------------------")
    print("Performing validation on the following DataFrame.")
    print("")
    print(df)
    print("")

    sblar_schema = get_schema_for_lei(lei)

    try:
        sblar_schema(df, lazy=True)
    except SchemaErrors as errors:
        for error in errors.schema_errors:
            # Name of the column in the dataframe being checked
            column_name = error["error"].schema.name

            # built in checks such as unique=True are different than custom
            # checks unfortunately so the name needs to be accessed differently
            try:
                check_name = error["error"].check.name
                # This will either be a boolean series or a single bool
                check_output = error["error"].check_output
            except AttributeError:
                check_name = error["error"].check
                # this is just a string that we'd need to parse manually
                check_output = error["error"].args[0]

            print(f"Validation `{check_name}` failed for column `{column_name}`")
            print(check_output)
            print("")


if __name__ == "__main__":
    csv_path = None
    lei: str = None
    if len(sys.argv) == 1:
        raise ValueError("csv_path arg not provided")
    elif len(sys.argv) == 2:
        csv_path = sys.argv[1]
    elif len(sys.argv) == 3:
        lei = sys.argv[1]
        csv_path = sys.argv[2]
    else:
        raise ValueError("correct number of args not provided")

    df = csv_to_df(csv_path)
    run_validation_on_df(df, lei)
