"""Test the ff module."""
import os
import pandas as pd
from unittest import TestCase

from dffiltering import ff


class testDataFrame(TestCase):
    def test_can_load_tab_as_DF(self):
        tab_file = os.path.join(os.path.dirname(__file__),
                                "SAMPLE.TVC.variants.tab")

        df = ff.load(tab_file)

        self.assertEqual(type(df), pd.DataFrame)
        # The DataFrame has 149 columns and 315 data rows.
        self.assertEqual(df.shape, (315, 149))
