# -*- coding: utf-8 -*-
"""
Functions to get CSV filenames and data.
"""

import re
from os import listdir
from os.path import isfile, join
from datetime import datetime
from itertools import product
import pandas as pd
import numpy as np

import covidcast
from .errors import APIDataFetchError

filename_regex = re.compile(
    r'^(?P<date>\d{8})_(?P<geo_type>\w+?)_(?P<signal>\w+)\.csv$')


def read_filenames(path):
    """
    Return a list of tuples of every filename and regex match to the CSV filename
     format in the specified directory.

    Arguments:
        - path: path to the directory containing CSV data files.

    Returns:
        - list of tuples
    """
    daily_filenames = [(f, filename_regex.match(f))
                       for f in listdir(path) if isfile(join(path, f))]
    return daily_filenames


def load_csv(path):
    """
    Load CSV with specified column types.
    """
    return pd.read_csv(
        path,
        dtype={
            'geo_id': str,
            'val': float,
            'se': float,
            'sample_size': float,
        })


def get_geo_sig_cmbo(data_source):
    """
    Get list of geo type-signal type combinations that we expect to see, based on
    combinations reported available by Covidcast metadata.
    """
    meta = covidcast.metadata()
    source_meta = meta[meta['data_source'] == data_source]
    unique_signals = source_meta['signal'].unique().tolist()
    unique_geotypes = source_meta['geo_type'].unique().tolist()

    if data_source == 'fb-survey':
        # Currently metadata returns --*community*-- signals that don't get generated
        # in the new fb-pipeline. Sieving them out for now.
        for sig in unique_signals:
            if "community" in sig:
                unique_signals.remove(sig)

    geo_sig_cmbo = list(product(unique_geotypes, unique_signals))
    print("Number of mixed types:", len(geo_sig_cmbo))

    return geo_sig_cmbo


def read_geo_sig_cmbo_files(geo_sig_cmbo, data_folder, filenames, date_slist):
    """
    Generator that assembles data within the specified date range for a given geo_sig_cmbo.

    Arguments:
        - geo_sig_cmbo: list of geo type-signal type combinations that we expect to see,
        based on combinations reported available by Covidcast metadata
        - data_folder: path to the directory containing CSV data files.
        - filenames: list of filenames
        - date_slist: list of dates (formatted as strings) to check

    Returns:
        - dataframe containing data for all dates in date_slist for a given
        geo type-signal type combination
        - relevant geo type (str)
        - relevant signal type (str)
    """
    for geo_sig in geo_sig_cmbo:
        df_list = list()

        # Get all filenames for this geo_type and signal_type
        files = [file for file in filenames if geo_sig[0]
                 in file and geo_sig[1] in file]

        if len(files) == 0:
            print("FILE_NOT_FOUND: File with geo_type:",
                  geo_sig[0], " and signal:", geo_sig[1], " does not exist!")
            yield pd.DataFrame(), geo_sig[0], geo_sig[1]
            continue

        # Load data from all found files.
        for file in files:
            data_df = load_csv(join(data_folder, file))
            for date in date_slist:

                # Add data's date, from CSV name, as new column
                if file.find(date) != -1:
                    source_date = datetime.strptime(date, '%Y%m%d')
                    data_df['time_value'] = source_date
            df_list.append(data_df)

        yield pd.concat(df_list), geo_sig[0], geo_sig[1]


def fetch_api_reference(data_source, start_date, end_date, geo, sig):
    """
    Get and process API data for use as a reference. Formatting is changed
    to match that of source data CSVs.
    """
    api_df = covidcast.signal(
        data_source, sig, start_date, end_date, geo)

    if not isinstance(api_df, pd.DataFrame):
        custom_msg = "Error fetching data from " + str(start_date) + \
                     " to " + str(end_date) + \
                     "for data source: " + data_source + \
                     ", signal-type: " + sig + \
                     ", geography-type: " + geo

        raise APIDataFetchError(custom_msg)

    column_names = ["geo_id", "val",
                    "se", "sample_size", "time_value"]

    # Replace None with NA to make numerical manipulation easier.
    # Rename and reorder columns to match those in df_to_test.
    api_df = api_df.replace(
        to_replace=[None], value=np.nan).rename(
        columns={'geo_value': "geo_id", 'stderr': 'se', 'value': 'val'}).drop(
        ['direction', 'issue', 'lag'], axis=1).reindex(columns=column_names)

    return api_df
