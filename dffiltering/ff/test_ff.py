"""Test the ff module."""
from os.path import dirname, join
import pandas as pd
import numpy as np
from unittest import TestCase

import ff


def file_test(filename):
    """Return the path to filename in test_files."""
    return join(dirname(__file__), "test_files", filename)


class testDataFrame(TestCase):
    def setUp(self):
        self.tab_file = join(dirname(__file__), "test_files", "8859.tab")
        self.tab2_file = join(
            dirname(__file__), "test_files", "DOT.column.tab")
        self.tab3_file = join(dirname(__file__), "test_files", "NA_fail.tab")
        self.tab4_file = join(
            dirname(__file__), "test_files", "str_num_fail.tab")

    def test_can_load_tab_as_DF(self):
        df = ff.load(self.tab_file)

        self.assertEqual(type(df), pd.DataFrame)
        # The DataFrame has 151 columns and 249 data rows.
        self.assertEqual(df.shape, (249, 151))

    def test_load_with_weird_chars(self):
        df = ff.load(self.tab_file)

        self.assertEqual(type(df), pd.DataFrame)
        # The DataFrame has 151 columns and 249 data rows.
        self.assertEqual(df.shape, (249, 151))

    def test_DF_has_loaded_correctly(self):
        df = ff.load(self.tab_file)

        self.assertEqual(df["MetaLR_score"].dtype, np.dtype("float64"))

    def test_DF_can_be_filtered_by_one_condition(self):
        df = ff.load(self.tab_file)

        self.assertEqual(ff.dffilter(['Ref == "G"'], df).shape, (60, 151))

        conditions = ['Func.refGene contains exonic']
        self.assertEqual(ff.dffilter(conditions, df).shape, (57, 151))

    def test_DF_can_be_filtered_by_two_conditions(self):
        df = ff.load(self.tab_file)

        conditions = ['Ref == "A"', 'Func.refGene contains exonic']

        self.assertEqual(ff.dffilter(conditions, df).shape, (13, 151))

    def test_DF_can_be_filtered_by_numeric_AND_string_conditions(self):
        df = ff.load(self.tab_file)

        conditions = ['PopFreqMax < 0.01', 'Func.refGene contains exonic']
        self.assertEqual(ff.dffilter(conditions, df).shape, (2, 151))

    def test_DF_can_be_filtered_with_OR_numeric_fields(self):
        df = ff.load(self.tab_file)

        conditions = ['PopFreqMax < 0.01 | PopFreqMax > 0.99',
                      'Func.refGene contains exonic']
        self.assertEqual(ff.dffilter(conditions, df).shape, (8, 151))

    def test_DF_can_be_filtered_with_OR_string_fields(self):
        df = ff.load(self.tab_file)

        conditions = ['PopFreqMax < 0.01 | PopFreqMax > 0.99',
                      'Func.refGene contains exonic|intronic']
        self.assertEqual(ff.dffilter(conditions, df).shape, (53, 151))

    def test_query_columns_with_dots(self):
        df = ff.load(self.tab2_file)

        conditions = ["TVC.counts < 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (8, 98))

        df = ff.load(self.tab2_file)  # The filtering of df is always in place

        conditions = ["TVC.counts > 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 98))

    def test_non_existent_columns_doesnt_break_code(self):
        df = ff.load(self.tab2_file)

        conditions = ["Imaginary < 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (9, 98))

    def test_multiple_weirdness_can_function(self):
        df = ff.load(self.tab2_file)

        conditions = ["TVC.counts < 3", "TVC.counts > 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (0, 98))

    def test_NaN_in_str_fields_dont_break_the_filter(self):
        df = ff.load(self.tab3_file)

        conditions = ['Func.refGene contains exonic|intronic']

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 76))

    def test_num_columns_that_fails_cast_to_str_coerced_into_nan(self):
        df = ff.load(self.tab4_file)

        conditions = ['CG46 != CG46']  # This is a trick to check if the column
                                       # has a NaN (NaN is not equal to itself)

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 76))


class testMainEntry(TestCase):
    def setUp(self):
        self.tab_file = file_test("8859.tab")
        self.json_filter = file_test("filter_sample.json")

    def test_main_entry_filter_correctly(self):
        class Arg(object):
            json_filter = self.json_filter
            filepath = self.tab_file
            column_contains = None
        args = Arg()

        df = ff.main(args)

        self.assertEqual(df.shape, (7, 151))

    def test_main_entry_filter_correctly_with_ext(self):
        class Arg(object):
            json_filter = self.json_filter
            filepath = self.tab_file
            column_contains = [file_test("Gene.refGene.txt")]
        args = Arg()

        df = ff.main(args)

        self.assertEqual(df.shape, (4, 151))


class testArgParser(TestCase):
    def setUp(self):
        self.tab_file = file_test("8859.tab")
        self.json_filter = file_test("filter_sample.json")
        self.gene_file = file_test("Gene.refGene")
        self.gene_file_ext = file_test("Gene.refGene.txt")

    def test_multiple_argument_parsing(self):
        args = ff.argparser([
            "--column-contains", "/path/to/Gene.refGene",
            "--column-contains", "/path/to/ExAC_ALL",
            "/path/to/filepath.tsv",
            "/path/to/filter.json"])

        self.assertTrue(args)
        self.assertCountEqual(args.column_contains,
                              ["/path/to/Gene.refGene", "/path/to/ExAC_ALL"])

    def test_multiple_argument_loading(self):
        args = ff.argparser([
            "--column-contains", self.gene_file,
            self.tab_file,
            self.json_filter])

        df = ff.main(args)

        self.assertEqual(df.shape, (4, 151))

    def test_extra_argument_contains_loader(self):
        self.file1 = file_test("CocaCola")
        conditions = ff.load_from_files(
            [self.file1, self.gene_file], "contains")

        self.assertCountEqual(conditions,
                              ["Gene.refGene contains PRH1|GRIN2B|FAKE3",
                               "CocaCola contains Azucar|Marron"])
