"""Test the ff module."""
import os
import pandas as pd
import numpy as np
from unittest import TestCase

from dffiltering import ff


class testDataFrame(TestCase):
    def setUp(self):
        self.tab_file = os.path.join(os.path.dirname(__file__), "8859.tab")

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

        self.assertEqual(ff.dffilter(df, ['Ref == "G"']).shape, (60, 151))
        self.assertEqual(
            ff.dffilter(df, ['Func.refGene contains exonic']).shape,
            (57, 151))

    def test_DF_can_be_filtered_by_two_conditions(self):
        df = ff.load(self.tab_file)

        self.assertEqual(
            ff.dffilter(
                df, ['Ref == "A"', 'Func.refGene contains exonic']).shape,
            (13, 151))

    def test_DF_can_be_filtered_by_numeric_AND_string_conditions(self):
        df = ff.load(self.tab_file)

        self.assertEqual(
            ff.dffilter(
                df, ['PopFreqMax < 0.01',
                     'Func.refGene contains exonic']).shape,
            (2, 151))

    def test_DF_can_be_filtered_with_OR_numeric_fields(self):
        df = ff.load(self.tab_file)

        self.assertEqual(
            ff.dffilter(
                df, ['PopFreqMax < 0.01 | PopFreqMax > 0.99',
                     'Func.refGene contains exonic']).shape,
            (8, 151))
