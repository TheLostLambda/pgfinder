"""Test the matching process"""

from pathlib import Path

import pandas as pd
import pytest

import pgfinder.matching as matching
from pgfinder.errors import UserError
from pgfinder.matching import calculate_ppm_delta, consolidate_results, pick_most_likely_structures

BASE_DIR = Path.cwd()
RESOURCES = BASE_DIR / "tests" / "resources"


def test_filtered_theo(raw_data, theo_masses, ppm):
    # this crude test just shows that the code runs
    # a better test would check that the data frame returned is correct
    matching.filtered_theo(raw_data, theo_masses, ppm)


def test_filtered_theo_no_match(raw_data_no_match, theo_masses, ppm):
    with pytest.raises(
        UserError,
        match="No matches were found for this search. Please check your database or increase mass tolerance.",
    ):
        matching.filtered_theo(raw_data_no_match, theo_masses, ppm)


def test_calculate_ppm_delta(sample_df: pd.DataFrame, df_diff_ppm: pd.DataFrame) -> None:
    """Test addition of PPM column."""
    pd.testing.assert_frame_equal(calculate_ppm_delta(sample_df, observed="obs", theoretical="exp"), df_diff_ppm)


def test_pick_most_likely_structures() -> None:
    """Test picking the most likely structure based on ppm"""
    long_df = pd.read_csv(RESOURCES / "long_results.csv")
    wide_df = pd.read_csv(RESOURCES / "wide_results.csv")

    reshaped_long_df = pick_most_likely_structures(long_df, 1)

    pd.testing.assert_frame_equal(reshaped_long_df, wide_df, check_dtype=False)


def test_consolidation() -> None:
    """Test the post-processing structure / intensity consolidation step"""
    unconsolidated_df = pd.read_csv(RESOURCES / "unconsolidated.csv")
    consolidated_df = pd.read_csv(RESOURCES / "consolidated.csv")

    # Duplicate column names are automatically mangled by read_csv seemingly
    # without any alternative, and comparing without the column names seems to
    # only be possible by dropping down to numpy via .values, but then that
    # chokes on NaN values, even with equal_nan=True, since it doesn't seem to
    # know the datatype of the column. I got sick of suffering, so this just
    # converts the numpy array to a string and compares those values.
    # Absolutely disgusting.
    assert str(consolidate_results(unconsolidated_df).values) == str(consolidated_df.values)
