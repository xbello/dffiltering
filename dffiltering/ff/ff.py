"""Deals with TAB files to load, munge and filter them."""
import logging
from os.path import basename, splitext
import re
from colorama import init, Fore, Style
import pandas as pd

init()  # Initialize colorama for windows

try:
    from .columns import COLUMN_TYPES
except (SystemError, ImportError):
    from columns import COLUMN_TYPES


logger = logging.getLogger("ff")


def clean(column, df):
    """Return the header/column in the DF cleaned from weird chars."""
    # Column names with dots, spaces, brackets... fail to do query
    weirds = [".", " "]
    new_column = column
    if any(_ in column for _ in weirds):
        for weird in weirds:
            new_column = new_column.replace(weird, "_")
        if column in df.columns:
            df.rename(columns={column: new_column}, inplace=True)
        # Replace all cases of this weird column

    # Fix the columns starting with numbers
    if re.match("[0-9^]+", column):
        new_column = "_" + column
        df.rename(columns={column: new_column}, inplace=True)

    return new_column, df


def error(text):
    """Colorize a text as error for the logs."""
    return "{}{}{}".format(Fore.RED, text, Style.RESET_ALL)


def dffilter(conditions, df):
    """Return a dataframe filtered by the conditions."""
    if not conditions:
        return df

    column, operator, terms = conditions[0].split(" ", 2)

    original_column = column

    if column not in df.columns:
        # As now this could come as file, trim the extension from the
        #  column name.
        column = splitext(column)[0]

    new_column, df = clean(column, df)
    conditions = [re.sub(r"\A" + column, new_column, _)
                  for _ in conditions]
    column = new_column

    if column in df.columns:
        if operator in ["contains"]:
            return dffilter(conditions[1:],
                            df[df[column].str.contains(terms, na=False)])

        if operator in ["not_contains"]:
            return dffilter(conditions[1:],
                            df[~df[column].str.contains(terms, na=False)])

        else:
            df.query(conditions[0], inplace=True)
            #return dffilter(conditions[1:], df)
    else:
        logger.error(
            error("Column not found ({}).".format(original_column)))

    # This column didn't exits, continue trying next columns
    return dffilter(conditions[1:], df)


def load(filepath):
    """Return the filepath loaded as a DataFrame.

    filepath is a path to either a .tab file or a .tab gzipped file.

    """
    # Explain: if dtype is not specified, read_table loads all the file into
    #  RAM (4 Gb), then infer types (down to 2 Gb) and then work. By loading
    #  everything as "object" we save the first pre-loading.
    if filepath.endswith(".gz"):
        from gzip import open as open_f
    else:
        open_f = open

    with open_f(filepath, "rb") as csv:
        header = {}.fromkeys(
            csv.readline().decode().rstrip().split("\t"), object)

    try:
        df = pd.read_table(filepath, dtype=header)
    except UnicodeDecodeError:
        df = pd.read_table(filepath, dtype=header, encoding="iso-8859-1")

    numeric_columns = [_ for _ in COLUMN_TYPES["numeric"] if _ in df.columns]

    for numeric_column in numeric_columns:
        # Correct columns with "," to ".".
        df[numeric_column] = df[numeric_column].str.replace(",", ".")
        # Correct columns with "." to zeroes.
        df[numeric_column].replace(".", 0, inplace=True)
        # Correct columns with "1." to ones.
        df[numeric_column].replace("1.", 1, inplace=True)
        # Replace - with zeroes
        df[numeric_column].replace("-", 0, inplace=True)
        # Fill the NaN with zeroes
        df[numeric_column].fillna(0, inplace=True)
        # Typecast the column into numeric hidding errors in NaN
        df[numeric_column] = pd.to_numeric(df[numeric_column], errors="coerce")

    # This could be faster than above line... but it isn't
    # df[numeric_columns] = df[numeric_columns].\
    #    apply(pd.to_numeric, errors="coerce")

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
    parser.add_argument("--filepath",
                        help="Path to the TSV file")
    parser.add_argument("--json-filter",
                        help="JSON file with list of filters")
    parser.add_argument(
        "--column-contains", action="append",
        help="""If you find more suitable to provide the filtering conditions
        as a txt list in a file, include as many columns as you need:

        --column-contains columnName --column-contains anotherCol""")

    parser.add_argument(
        "--numeric-cols",
        type=lambda s: [_ for _ in s.split(',')],
        help="""If you have numeric columns added to your .tsv file that are
        not in the default ones, you'll have to include them in this flag:

        --numeric-cols columnName
        --numeric-cols columnNameA,columnNameB""")

    parser.add_argument("--version", "-v", action="store_true")

    return parser.parse_args(args)


def main(args):  # json_filter, filepath, column_contains=None):
    """Return a filtered DF per json_filter."""
    if getattr(args, "version", None):
        from . import _version
        print(_version.__version__)

    filters = []
    if args.json_filter:
        import json

        with open(args.json_filter) as js_filter:
            filters = json.load(js_filter)

    if getattr(args, "column_contains", None):
        # Load the extra conditions passed
        filters.extend(load_from_files(args.column_contains, "contains"))

    if getattr(args, "numeric_cols", None):
        # Load the extra columns defined as numeric
        COLUMN_TYPES["numeric"].extend(args.numeric_cols)

    if args.filepath:
        df = dffilter(filters, load(args.filepath))

        return df


if __name__ == "__main__":
    import sys
    p_args = argparser(sys.argv[1:])
    d_f = main(p_args)

    if d_f:
        print(d_f.to_csv(sep="\t", index=False))
