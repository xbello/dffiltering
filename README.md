# dffiltering

## Requirements

Python >= 3.4, Pandas >= 0.19.1

## Install
The source code is currently hosted on GitHub at:
http://github.com/xbello/dffiltering

```sh
pip3 install git+git://github.com/xbello/dffiltering
```

## Update

```sh
pip3 install git+git://github.com/xbello/dffiltering --upgrade
```

There's a chance the previous don't work. You'll have to try to download the
whole package (https://github.com/xbello/dffiltering/archive/master.zip),
unzip it, open a command line to the unzipped folder that should contain some
`setup.py` file and write this:

```sh
python setup.py install
```

## Usage

First of all get a brief read of the command help with:

```sh
dff -h
```

You'll need a TSV file and a json file with all the filtering conditions. The json file list all the filters to apply cummulatively to the TSV, like [this](https://raw.githubusercontent.com/xbello/dffiltering/master/ff/test_files/filter_sample.json):

    ["vardb_gatk <= 20",
     "vardb_tvc <= 20",
     "ExAC_ALL <= 0.1 | ExAC_ALL >= 0.9",
     "Func.refGene contains exonic|splicing"
    ]

The `string` filtering operations can be `contains` or `not_contains`. In the edge case that you need to find a columns that contains "XXX" but no "ZZZXXX" use a RegExp like `Func.refGene contains \WXXX` (backslash and capital W): the `\W` marker matches anything that is not a char e.g. spaces, tabs and semicolons.

Then you can call the filtering from the command line:

```sh
dff --filepath path/to/tabfile.tsv --json_filter path/to/filters.json
```

### Big "contains"

If you ever need a lot of "contains" you can either try to transform your list
into a nice JSON condition:

Contents of `Gene.refGene`:

        GENE1
        GENE2
        ...
        GENEX

and hen execute this command to create the JSON filter.

    $ tr "\r\n" "|" < Gene.refGene
    GENE1|GENE2| ... |GENEX

Or you can pass a filename matching a column name to the program:

    dff --filepath path/to/tabfile.tsv --json_filter path/to/filters.json --column-contains path/to/Gene.refGene

This can be done with multiple columns:

    dff --filepath path/to/tabfile.tsv --json_filter path/to/filters.json --column-contains path/to/Gene.refGene --column-contains path/to/ExAC_ALL

> Note the file is named 'Gene.refGene' and not 'Gene.refGene.txt'.

# Troubleshotting

...
