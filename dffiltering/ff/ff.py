"""Deals with TAB files to load, munge and filter them."""
from os.path import basename
import pandas as pd

try:
    from .columns import COLUMN_TYPES
    # XXX Users should be able to aport their own column_types
except (SystemError, ImportError):
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
                            df[df[column].str.contains(terms, na=False)])

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

    df[numeric_columns] = df[numeric_columns].\
        apply(pd.to_numeric, errors="coerce")

    return df


def load_from_files(filepaths, condition):
    """Return a list of conditions loaded from text files."""
    conds = []
    for column in filepaths:
        column_name = basename(column)
        with open(column) as contains:
            conditions = "|".join([_.rstrip() for _ in contains])
        conds.append("{} {} {}".format(
            column_name, condition, conditions))

    return conds


def argparser(args):
    """Return the parsed arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="DataFrame Filtering")
    parser.add_argument("filepath",
                        help="Path to the TSV file")
    parser.add_argument("json_filter",
                        help="JSON file with list of filters")
    parser.add_argument(
        "--column-contains", action="append",
        help="""If you find more suitable to provide the filtering conditions
        as a txt list in a file, include as many columns as you need:

        --column-contains columnName --column-contains anotherCol""")

    return parser.parse_args(args)


def main(args):  # json_filter, filepath, column_contains=None):
    """Return a filtered DF per json_filter."""
    import json

    filters = {}
    with open(args.json_filter) as js_filter:
        filters = json.load(js_filter)

    if hasattr(args, "column_contains"):
        # Load the extra conditions passed
        filters.extend(load_from_files(args.column_contains, "contains"))

    df = dffilter(filters, load(args.filepath))

    return df


if __name__ == "__main__":
    import sys
    p_args = argparser(sys.argv[1:])
    d_f = main(p_args)

    print(d_f.to_csv(sep="\t", index=False))
