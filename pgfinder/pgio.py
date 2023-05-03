"""PG Finder I/O operations"""
import logging
import tempfile
from typing import Union, Dict
from pathlib import Path
from datetime import datetime
import io
import pandas as pd
import sqlite3
import numpy as np
import yaml

from ruamel.yaml import YAML, YAMLError

from pgfinder.logs.logs import LOGGER_NAME
from pgfinder._version import get_versions

LOGGER = logging.getLogger(LOGGER_NAME)


def ms_file_reader(file) -> pd.DataFrame:
    """Read mass spec data.

    Parameters
    ----------
    file: Union[str, Path]
        Path to be loaded.

    Returns
    -------
    pd.DataFrame
        File loaded as Pandas Dataframe.
    """
    filename = file
    if not str(file).find("ftrs") == -1:
        return_df = ftrs_reader(file)
    elif not str(file).find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["file"] = filename
    LOGGER.info(f"Mass spectroscopy file loaded from : {file}")
    print(return_df.head())
    print(return_df.tail())
    return return_df


def ms_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading from an interactive jupyter notebook with a file upload widget.

    Parameters
    ----------
    upload: dict
        Dictionary of properties of a file uploaded using `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#File-Upload>`_

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of mass information
    """
    filename = upload["name"]
    file_contents = upload["content"]
    file_temp = tempfile.NamedTemporaryFile(delete=False)
    file_temp.write(file_contents)
    file = file_temp.name

    if not filename.find("ftrs") == -1:
        return_df = ftrs_reader(file)
    elif not filename.find("txt") == -1:
        return_df = maxquant_file_reader(file)
    else:
        raise ValueError("Unknown file type.")

    return_df.attrs["file"] = filename
    LOGGER.info(f"Mass spectroscopy file loaded from  : {filename}")
    print(return_df.head())
    print(return_df.tail())
    return return_df


def ftrs_reader(file: Union[str, Path]) -> pd.DataFrame:
    """Reads Features file from Byos

    Parameters
    ----------
    file: Union[str, Path]
        Feature file to be read.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of features.
    """
    with sqlite3.connect(file) as db:
        sql = "SELECT * FROM Features"
        # Reads sql database into dataframe
        ff = pd.read_sql(sql, db)
        # Adds empty "Inferred structure" and "Theo (Da)" columns
        ff["Inferred structure"] = np.nan
        ff["Theo (Da)"] = np.nan
        # Renames columns to expected column heading required for data_analysis function
        ff.rename(
            columns={
                "Id": "ID",
                "ionCount": "Ion count",
                "chargeOrder": "Charge state",
                "xicStart": "XIC start (min)",
                "xicEnd": "XIC end (min)",
                "apexRetentionTimeMinutes": "RT (min)",
                "apexMwMonoisotopic": "Obs (Da)",
                "maxIntensity": "Intensity",
                "maxAveragineCorrelation": "corrMax",
            },
            inplace=True,
        )
        # Reorder columns in dataframe to desired order, dropping unwanted columns
        cols_order = [
            "ID",
            "Ion count",
            "Charge state",
            "XIC start (min)",
            "XIC end (min)",
            "RT (min)",
            "Obs (Da)",
            "Theo (Da)",
            "Inferred structure",
            "Intensity",
        ]
        ff = ff[cols_order]

        return ff


def theo_masses_reader(input_file: Union[str, Path]) -> pd.DataFrame:
    """Reads theoretical masses files (csv) returning a Panda Dataframe

    Parameters
    ----------
    input_file: Union[str, Path]

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame of theoretical masses.
    """
    theo_masses_df = pd.read_csv(input_file)
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = input_file
    LOGGER.info(f"Theoretical masses loaded from     : {input_file}")
    print(theo_masses_df.head())
    print(theo_masses_df.tail())
    return theo_masses_df


def theo_masses_upload_reader(upload: dict) -> pd.DataFrame:
    """For reading theoretical masses from an interactive jupyter notebook with a file upload widget.

    Parameters
    ----------
    upload: dict
        Dictionary of properties of a file uploaded using `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#File-Upload>`_

    Returns
    -------
    pd.DataFrame
        Pandas Dataframe of theoretical masses.
    """

    filename = upload["name"]
    file_contents = upload["content"]

    theo_masses_df = pd.read_csv(io.BytesIO(file_contents))
    theo_masses_df.columns = ["Inferred structure", "Theo (Da)"]
    theo_masses_df.attrs["file"] = filename
    LOGGER.info(f"Theoretical masses loaded from     : {filename}")
    print(theo_masses_df.head())
    print(theo_masses_df.tail())
    return theo_masses_df


def maxquant_file_reader(file):
    """Reads maxquant files and outputs data as a dataframe.

    Parameters
    ----------
    filepath: Union[str, Path]
        Path to a text file.

    Returns
    -------
    pd.DataFrame
        Pandas Data frame
    """

    # reads file into dataframe
    maxquant_df = pd.read_table(file, low_memory=False)
    # adds inferredStructure column
    maxquant_df["Inferred structure"] = np.nan
    # adds theo_mwMonoisotopic column
    maxquant_df["Theo (Da)"] = np.nan
    # insert dataframe index as a column
    maxquant_df.reset_index(level=0, inplace=True)
    # Renames columns to expected column heading required for data_analysis function
    maxquant_df.rename(
        columns={
            "index": "ID",
            "Retention time": "RT (min)",
            "Retention length": "RT (length)",
            "Mass": "Obs (Da)",
            "Intensity": "Intensity",
        },
        inplace=True,
    )
    # Desired variables and order
    cols_order = [
        "ID",
        "RT (min)",
        "RT (length)",
        "Obs (Da)",
        "Theo (Da)",
        "Inferred structure",
        "Intensity",
    ]
    # Reorder columns in dataframe to desired order.
    maxquant_df = maxquant_df[cols_order]

    return maxquant_df


def dataframe_to_csv(
    save_filepath: Union[str, Path], filename: str, output_dataframe: pd.DataFrame, float_format: str = "%.4f"
) -> None:
    """
    Writes dataframe to csv file at desired file location

    Parameters
    ----------
    save_filepath: Union[str, Path]
        Directory to save tile to.
    filename: str
        Filename to save file to.
    output_dataframe: pd.DataFrame
        Pandas Dataframe to write to csv
    float_format: str
        Format for floating point numbers (default 4 decimal places)
    """
    # Combine save location and desired file name with correct formatting for output as csv file.
    output_dataframe.to_csv(Path(save_filepath) / filename, index=False, float_format=float_format)


def dataframe_to_csv_metadata(
    output_dataframe: pd.DataFrame,
    save_filepath: Union[str, Path] = None,
    filename: Union[str, Path] = None,
    float_format: str = "%.4f",
) -> Union[str, Path]:
    """If save_filepath is specified return the relative path of the output file, including the filename, otherwise
    return the .csv in the form of a string.

    Parameters
    ----------
    output_dataframe: pd.DataFrame
        Dataframe to output.
    save_filepath: Union[str, Path]
        Path to save to.
    filename: Union[str, Path]
        Filename to save to.
    float_format: str
        Format for floating point numbers (default 4 decimal places)

    Returns
    -------
    """
    metadata = {
        "file": str(output_dataframe.attrs["file"]),
        "masses_file": str(output_dataframe.attrs["masses_file"]),
        "rt_window": output_dataframe.attrs["rt_window"],
        "modifications": output_dataframe.attrs["modifications"],
        "ppm": output_dataframe.attrs["ppm"],
        "version": get_versions()["version"],
    }

    metadata_string = yaml.dump(metadata)
    # Using pathlib we replace '\' if on Windows to '/' so tests pass
    metadata_string = metadata_string.replace("\\", "/")
    output_dataframe.insert(0, metadata_string.replace("\n", " "), "")

    # We're going to actually save the file to disk
    if save_filepath:
        filename = filename if filename is not None else default_filename()
        save_filepath = Path(save_filepath)
        save_filepath.mkdir(parents=True, exist_ok=True)
        output_dataframe.to_csv(save_filepath / filename, index=False, float_format=float_format)
        output = str(save_filepath / filename)
    # We're going to leave it in memory as a string
    else:
        output = output_dataframe.to_csv(index=False, float_format=float_format)

    return output


def default_filename(prefix: str = "results_") -> str:
    """Generate a default filename based on the current date/time.

    Returns
    -------
    str
        Filename with format 'results_YYYY-MM-DD-hh-mm-ss.csv'.
    """
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = prefix + date_time + ".csv"

    return filename


def read_yaml(filename: Union[str, Path]) -> Dict:
    """Read a YAML file.

    Parameters
    ----------
    filename: Union[str, Path]
        YAML file to read.

    Returns
    -------
    Dict
        Dictionary of the file."""

    with Path(filename).open() as f:
        try:
            yaml_file = YAML(typ="safe")
            return yaml_file.load(f)
        except YAMLError as exception:
            LOGGER.error(exception)
            return {}
