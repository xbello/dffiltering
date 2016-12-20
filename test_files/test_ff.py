"""Test the ff module."""
import os
import pandas as pd
import numpy as np
from unittest import TestCase

from dffiltering import ff


class testDataFrame(TestCase):
    def setUp(self):
        self.tab_file = os.path.join(os.path.dirname(__file__), "8859.tab")
        self.tab2_file = os.path.join(os.path.dirname(__file__),
                                      "DOT.column.tab")

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


class testMainEntry(TestCase):
    def setUp(self):
        self.tab_file = os.path.join(os.path.dirname(__file__), "8859.tab")
        self.json_filter = os.path.join(os.path.dirname(__file__),
                                        "filter_sample.json")

    def test_main_entry_filter_correctly(self):
        df = ff.main(self.json_filter, self.tab_file)

        self.assertEqual(df.shape, (7, 151))
