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


## Usage

You'll need a TSV file and a json file with all the filtering conditions. The json file list all the filters to apply cummulatively to the TSV, like [this](https://raw.githubusercontent.com/xbello/dffiltering/master/ff/test_files/filter_sample.json):

    ["vardb_gatk <= 20",
     "vardb_tvc <= 20",
     "ExAC_ALL <= 0.1 | ExAC_ALL >= 0.9",
     "Func.refGene contains exonic|splicing"
    ]

Then you can call the filtering from the command line:

```sh
dff path/to/tabfile.tsv path/to/filters.json
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

    dff path/to/tabfile.tsv path/to/filters.json --column-contains path/to/Gene.refGene

This can be done with multiple columns:

    dff path/to/tabfile.tsv path/to/filters.json --column-contains path/to/Gene.refGene --column-contains path/to/ExAC_ALL

> Note the file is named 'Gene.refGene' and not 'Gene.refGene.txt'.

# Troubleshotting

...
