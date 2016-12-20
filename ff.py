"""Deals with TAB files to load, munge and filter them."""
import pandas as pd

from dffiltering.columns import COLUMN_TYPES  # XXX Users should be able to
  # aport their own column_types


def dffilter(df, conditions):
    """Return a dataframe filtered by the conditions."""
    if not conditions:
        return df

    condition = conditions.pop()

    if "contains" in condition:
        column, query = condition.split(" contains ")
        if column in df.columns:
            return dffilter(df[df[column].str.contains(query)], conditions)

    else:
        # Names with dots, spaces, brackets... fail to do query
        column = condition.split()[0]
        if column in df.columns:
            new_column = column
            for weird in [".", " "]:
                new_column = new_column.replace(weird, "_")
            df.rename(columns={column: new_column}, inplace=True)

            condition = condition.replace(column, new_column)

            return dffilter(df.query(condition), conditions)

    # This column didn't exits, continue trying next columns
    return dffilter(df, conditions)


def load(filepath):
    """Return the filepath loaded as a DataFrame."""
    try:
        df = pd.read_table(filepath)
    except UnicodeDecodeError:
        df = pd.read_table(filepath, encoding="iso-8859-1")

    # Correct columns with "." to zeroes.
    df.replace(".", 0, inplace=True)
    # Correct columns with "1." to ones.
    df.replace("1.", 1, inplace=True)
    # Fill the NaN with zeroes
    df.fillna(0, inplace=True)

    df[COLUMN_TYPES["numeric"]] = df[COLUMN_TYPES["numeric"]].\
        apply(pd.to_numeric)

    return df


def argparser():
    """Return the parsed arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="DataFrame Filtering")
    parser.add_argument("filepath",
                        help="Path to the TSV file")
    parser.add_argument("json_filter",
                        help="JSON file with list of filters")

    return parser


def main(filepath, json_filter):
    """Return a filtered DF per json_filter."""
    import json

    with open(json_filter) as js_filter:
        df = dffilter(load(filepath), json.load(js_filter))

    return df


if __name__ == "__main__":
    import sys
    args = argparser().parse_args(sys.argv[1:])
    d_f = main(args.filepath, args.json_filter)

    print(d_f.to_csv(sep="\t", index=False))
