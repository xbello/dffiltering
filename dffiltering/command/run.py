import sys
from dffiltering.ff import ff


def run():
    args = ff.argparser(sys.argv[1:])

    if args:
        df = ff.main(args)
        print(df.to_csv(sep="\t", index=False))


if __name__ == "__main__":
    run()
