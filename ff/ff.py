"""Deals with TAB files to load, munge and filter them."""
import pandas as pd

from columns import COLUMN_TYPES  # XXX Users should be able to
  # aport their own column_types


def dffilter(conditions, df, i=0):
    """Return a dataframe filtered by the conditions."""
    if len(conditions) <= i:
        return df

    condition = conditions[i]

    if "contains" in condition:
        column, query = condition.split(" contains ")
        if column in df.columns:
            return dffilter(conditions,
                            df[df[column].str.contains(query)],
                            i + 1)

    else:
        # Names with dots, spaces, brackets... fail to do query
        column = condition.split()[0]
        if column in df.columns:
            new_column = column
            for weird in [".", " "]:
                new_column = new_column.replace(weird, "_")
            df.rename(columns={column: new_column}, inplace=True)

            condition = condition.replace(column, new_column)

            return dffilter(conditions, df.query(condition), i + 1)

    # This column didn't exits, continue trying next columns
    return dffilter(conditions, df, i + 1)


def load(filepath):
    """Return the filepath loaded as a DataFrame."""
    try:
        df = pd.read_table(filepath)
    except UnicodeDecodeError:
        df = pd.read_table(filepath, encoding="iso-8859-1")

    numeric_columns = [_ for _ in COLUMN_TYPES["numeric"] if _ in df.columns]

    for numeric_column in numeric_columns:
        # Correct columns with "." to zeroes.
        df[numeric_column].replace(".", 0, inplace=True)
        # Correct columns with "1." to ones.
        df[numeric_column].replace("1.", 1, inplace=True)
        # Replace - with zeroes
        df[numeric_column].replace("-", 0, inplace=True)
        # Fill the NaN with zeroes
        df[numeric_column].fillna(0, inplace=True)

    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

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


def main(json_filter, filepath):
    """Return a filtered DF per json_filter."""
    import json

    with open(json_filter) as js_filter:
        df = dffilter(json.load(js_filter), load(filepath))

    return df


if __name__ == "__main__":
    import sys
    args = argparser().parse_args(sys.argv[1:])
    d_f = main(args.json_filter, args.filepath)

    print(d_f.to_csv(sep="\t", index=False))
