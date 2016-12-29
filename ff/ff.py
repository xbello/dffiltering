"""Deals with TAB files to load, munge and filter them."""
import pandas as pd

try:
    from ff.columns import COLUMN_TYPES  # XXX Users should be able to
                                         # aport their own column_types
except ImportError:
    from columns import COLUMN_TYPES


def dffilter(conditions, df):
    """Return a dataframe filtered by the conditions."""
    if not conditions:
        return df

    column, operator, terms = conditions[0].split(" ", 2)

    # Column names with dots, spaces, brackets... fail to do query
    weirds = [".", " "]
    if any(_ in column for _ in weirds):
        new_column = column
        for weird in weirds:
            new_column = new_column.replace(weird, "_")
        if column in df.columns:
            df.rename(columns={column: new_column}, inplace=True)
        conditions[0] = conditions[0].replace(column, new_column)
        return dffilter(conditions, df)


    if operator in ["contains"]:
        if column in df.columns:
            return dffilter(conditions[1:],
                            df[df[column].str.contains(terms)])

    else:
        if column in df.columns:
            return dffilter(conditions[1:], df.query(conditions[0]))

    # This column didn't exits, continue trying next columns
    return dffilter(conditions[1:], df)


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
