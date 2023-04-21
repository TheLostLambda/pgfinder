"""Test the matching process"""
import pytest

import pandas as pd

import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation
from pgfinder.matching import calculate_ppm_delta, determine_most_likely_structure, consolidate_matches


def test_filtered_theo(raw_data, theo_masses, ppm):
    # this crude test just shows that the code runs
    # a better test would check that the data frame returned is correct
    matching.filtered_theo(raw_data, theo_masses, ppm)


def test_filtered_theo_no_match(raw_data_no_match, theo_masses, ppm):
    with pytest.raises(
        ValueError,
        match="NO MATCHES WERE FOUND for this search. Please check your database or increase mass tolerance.",
    ):
        matching.filtered_theo(raw_data_no_match, theo_masses, ppm)


def test_calculate_ppm_delta(sample_df: pd.DataFrame, df_diff_ppm: pd.DataFrame) -> None:
    """Test addition of PPM column."""
    pd.testing.assert_frame_equal(calculate_ppm_delta(sample_df, observed="obs", theoretical="exp"), df_diff_ppm)


def test_determine_most_likely_structure(df_diff_ppm: pd.DataFrame, df_lowest_ppm: pd.DataFrame) -> None:
    """Test determining the most likely structure."""
    pd.testing.assert_frame_equal(
        determine_most_likely_structure(df=df_diff_ppm, id="id", diff="diff_ppm", intensity="intensity"), df_lowest_ppm
    )


def test_consolidate_matches(df_likely_structure: pd.DataFrame, consolidated: pd.DataFrame) -> None:
    """Test consolidation."""
    print(f"df_likely_structure :\n{df_likely_structure}")
    pd.testing.assert_frame_equal(
        consolidate_matches(
            df=df_likely_structure,
            id="id",
            inferred="inferred",
            lowest_ppm="lowest ppm",
            intensity="Inferred Max Intensity",
        ),
        consolidated,
    )
