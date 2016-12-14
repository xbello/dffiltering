"""Deals with TAB files to load, munge and filter them."""
import pandas as pd


def load(filepath):
    """Return the filepath loaded as a DataFrame."""
    return pd.read_table(filepath)
