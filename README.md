# dffiltering

## Requirements

Python >= 3.4, Pandas >= 0.19.1

## Install
The source code is currently hosted on GitHub at:
http://github.com/xbello/dffiltering

```sh
pip3 install git+git://github.com/xbello/dffiltering
```

## Usage

You'll need a TSV file and a json file with all the filtering conditions. The json file list all the filters to apply cummulatively to the TSV, like [this](https://raw.githubusercontent.com/xbello/dffiltering/master/ff/test_files/filter_sample.json):

    ["vardb_gatk <= 20",
     "vardb_tvc <= 20",
     "ExAC_ALL <= 0.1",
     "Func.refGene contains exonic|splicing"
    ]

Then you can call the filtering from the command line:

```sh
dff path/to/tabfile.tsv path/to/filters.json
```

# Troubleshotting

...
