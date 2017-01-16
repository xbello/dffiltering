import argparse
from ff import ff


def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter a file per JSON conditions")
    parser.add_argument("tsv",
                        help="A .tsv file path.")
    parser.add_argument("json",
                        help="A .json file path.")

    return parser.parse_args()


def run():
    args = parse_args()

    if args:
        df = ff.main(args.json, args.tsv)
        print(df.to_csv(sep="\t", index=False))

if __name__ == "__main__":
    run()
