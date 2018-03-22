"""Test the ff module."""
import json
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

    def test_can_load_gzipped_tab_as_DF(self):
        df = ff.load(self.tab_file + ".gz")

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

    def test_DF_can_be_filtered_by_one_condition_query(self):
        df = ff.load(self.tab_file)

        self.assertEqual(ff.dffilter(['Ref == "G"'], df).shape, (60, 151))

    def test_DF_can_be_filtered_by_one_condition_contains(self):
        df = ff.load(self.tab_file)

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

        self.assertEqual(ff.dffilter(conditions, df).shape, (8, 99))

        df = ff.load(self.tab2_file)  # The filtering of df is always in place

        conditions = ["TVC.counts > 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 99))

    def test_non_existent_columns_doesnt_break_code(self):
        df = ff.load(self.tab2_file)

        conditions = ["Imaginary < 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (9, 99))

    def test_multiple_weirdness_can_function(self):
        df = ff.load(self.tab2_file)

        conditions = ["TVC.counts < 3", "TVC.counts > 3"]

        self.assertEqual(ff.dffilter(conditions, df).shape, (0, 99))

    def test_NaN_in_str_fields_dont_break_the_filter(self):
        df = ff.load(self.tab3_file)

        conditions = ['Func.refGene contains exonic|intronic']

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 76))

    def test_num_columns_that_fails_cast_to_str_coerced_into_nan(self):
        df = ff.load(self.tab4_file)

        conditions = ['CG46 != CG46']  # This is a trick to check if the column
                                       # has a NaN (NaN is not equal to itself)

        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 76))

    def test_num_columns_with_commas(self):
        tab_file = join(dirname(__file__), "test_files", "floats_comma.tab")
        df = ff.load(tab_file)

        self.assertEqual(ff.dffilter(['ExAC_ALL <= 0.1'], df).shape, (5, 2))


class testFilterAndDFClean(TestCase):
    def test_cleansing_filter_and_df(self):
        tab_file = file_test("DOT.column.tab")
        column = "TVC.counts"
        df = ff.load(tab_file)

        self.assertTrue("TVC.counts" in df.columns)

        column, df = ff.clean(column, df)

        self.assertEqual("TVC_counts", column)
        self.assertTrue("TVC_counts" in df.columns)

    def test_cleansing_filter_number_starting_column(self):
        tab_file = file_test("DOT.column.tab")
        column = "1000G_ALL"
        df = ff.load(tab_file)

        self.assertTrue("1000G_ALL" in df.columns)

        column, df = ff.clean(column, df)

        self.assertEqual("_1000G_ALL", column)
        self.assertTrue("_1000G_ALL" in df.columns)

    def test_reverse_the_filter_condition_single(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = ['Func.refGene not_contains intronic']
        self.assertEqual(ff.dffilter(conditions, df).shape, (4, 99))

    def test_reverse_the_filter_condition_multiple(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = ['ExonicFunc.refGene not_contains frameshift deletion']
        self.assertEqual(ff.dffilter(conditions, df).shape, (8, 99))

    def test_reverse_the_filter_condition_similar_words(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = [r'ExonicFunc.refGene not_contains \bsynonymous SNV']
        self.assertEqual(ff.dffilter(conditions, df).shape, (8, 99))

    def test_reverse_the_filter_condition_similar_words_and_or(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = [
            r'ExonicFunc.refGene not_contains \bsynonymous SNV|deletion']
        self.assertEqual(ff.dffilter(conditions, df).shape, (7, 99))

    def test_reverse_the_filter_condition_similar_ords_and_or_json(self):
        conds = json.load(open(file_test("slashb.json")))
        df = ff.load(file_test("DOT.column.tab"))

        new_df = ff.dffilter(conds, df)

        self.assertEqual(new_df.shape, (4, 99))

    def test_news_filter_2017_03(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = ['gnomAD_exome_ALL > 0.99']
        self.assertEqual(ff.dffilter(conditions, df).shape, (2, 99))

    def test_thousand_genomes_column_filtering(self):
        df = ff.load(file_test("DOT.column.tab"))

        conditions = ['1000G_ALL > 0.2']
        self.assertEqual(ff.dffilter(conditions, df).shape, (1, 99))


class testMainEntry(TestCase):
    def setUp(self):
        self.tab_file = file_test("8859.tab")
        self.json_filter = file_test("filter_sample.json")

        class Arg(object):
            json_filter = self.json_filter
            filepath = self.tab_file
            column_contains = None

        self.args = Arg()

    def test_main_entry_filter_correctly(self):
        df = ff.main(self.args)

        self.assertEqual(df.shape, (7, 151))

    def test_main_entry_filter_correctly_with_ext(self):
        class Arg(object):
            json_filter = self.json_filter
            filepath = self.tab_file
            column_contains = [file_test("Gene.refGene.txt")]
        args = Arg()

        df = ff.main(args)

        self.assertEqual(df.shape, (4, 151))

    def test_main_entry_with_extra_columns(self):
        self.args.filepath = file_test("Ten.columns.tab")
        self.args.json_filter = file_test("extra_cols.json")
        self.args.numeric_cols = ["MakeUp.Name", "Other.Column"]

        df = ff.main(self.args)

        self.assertEqual(df.shape, (1, 10))


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
            "--filepath", "/path/to/filepath.tsv",
            "--json-filter", "/path/to/filter.json"])

        self.assertTrue(args)
        self.assertCountEqual(args.column_contains,
                              ["/path/to/Gene.refGene", "/path/to/ExAC_ALL"])

    def test_multiple_argument_loading(self):
        args = ff.argparser([
            "--column-contains", self.gene_file,
            "--filepath", self.tab_file,
            "--json-filter", self.json_filter])

        df = ff.main(args)

        self.assertEqual(df.shape, (4, 151))

    def test_extra_argument_contains_loader(self):
        file1 = file_test("CocaCola")
        conditions = ff.load_from_files([file1, self.gene_file], "contains")

        self.assertCountEqual(conditions,
                              ["Gene.refGene contains PRH1|GRIN2B|FAKE3",
                               "CocaCola contains Azucar|Marron"])

    def test_naming_new_numeric_columns(self):
        args = ff.argparser([
            "--numeric-cols", "MakeUp.Name",
            "--filepath", "/path/to/filepath.tsv",
            "--json-filter", "/path/to/filter.json"])

        self.assertTrue(args)
        self.assertCountEqual(args.numeric_cols, ["MakeUp.Name"])

        args = ff.argparser([
            "--numeric-cols", "MakeUp.Name,Other.Name",
            "--filepath", "/path/to/filepath.tsv",
            "--json-filter", "/path/to/filter.json"])

        self.assertCountEqual(args.numeric_cols, ["MakeUp.Name", "Other.Name"])
