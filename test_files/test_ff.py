"""Test the ff module."""
import os
import pandas as pd
import numpy as np
from unittest import TestCase

from dffiltering import ff


class testDataFrame(TestCase):
    def test_can_load_tab_as_DF(self):
        tab_file = os.path.join(os.path.dirname(__file__),
                                "8859.tab")

        df = ff.load(tab_file)

        self.assertEqual(type(df), pd.DataFrame)
        # The DataFrame has 149 columns and 315 data rows.
        self.assertEqual(df.shape, (249, 151))

    def test_load_with_weird_chars(self):
        tab_file = os.path.join(os.path.dirname(__file__),
                                "8859.tab")

        df = ff.load(tab_file)

        self.assertEqual(type(df), pd.DataFrame)
        # The DataFrame has 149 columns and 315 data rows.
        self.assertEqual(df.shape, (249, 151))

    def test_DF_has_loaded_correctly(self):
        tab_file = os.path.join(os.path.dirname(__file__), "8859.tab")

        df = ff.load(tab_file)

        self.assertEqual(df["MetaLR_score"].dtype, np.dtype("float64"))
