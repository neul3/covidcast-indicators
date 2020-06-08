# -*- coding: utf-8 -*-
import pandas as pd


INCIDENCE_BASE = 100000
# https://code.activestate.com/recipes/577775-state-fips-codes-dict/
STATE_TO_FIPS = {
    "WA": "53",
    "DE": "10",
    "DC": "11",
    "WI": "55",
    "WV": "54",
    "HI": "15",
    "FL": "12",
    "WY": "56",
    "PR": "72",
    "NJ": "34",
    "NM": "35",
    "TX": "48",
    "LA": "22",
    "NC": "37",
    "ND": "38",
    "NE": "31",
    "TN": "47",
    "NY": "36",
    "PA": "42",
    "AK": "02",
    "NV": "32",
    "NH": "33",
    "VA": "51",
    "CO": "08",
    "CA": "06",
    "AL": "01",
    "AR": "05",
    "VT": "50",
    "IL": "17",
    "GA": "13",
    "IN": "18",
    "IA": "19",
    "MA": "25",
    "AZ": "04",
    "ID": "16",
    "CT": "09",
    "ME": "23",
    "MD": "24",
    "OK": "40",
    "OH": "39",
    "UT": "49",
    "MO": "29",
    "MN": "27",
    "MI": "26",
    "RI": "44",
    "KS": "20",
    "MT": "30",
    "MS": "28",
    "SC": "45",
    "KY": "21",
    "OR": "41",
    "SD": "46",
}
DN_FIPS = "70002"
DUKES_FIPS = "25007"
NANTU_FIPS = "25019"
DN_COUNTY_FIPS = [
    DUKES_FIPS,
    NANTU_FIPS,
]
KC_FIPS = "70003"
KC_COUNTY_FIPS = [
    "29095",  # Jackson
    "29165",  # Platte
    "29037",  # Cass
    "29047",  # Clay
]
SECONDARY_FIPS = [
    ("51620", ["51093", "51175"]),
    ("51685", ["51153"]),
    ("28039", ["28059", "28041", "28131", "28045", "28059", "28109", "28047"]),
    ("51690", ["51089", "51067"]),
    ("51595", ["51081", "51025", "51175", "51183"]),
    ("51600", ["51059", "51059", "51059"]),
    ("51580", ["51005"]),
    ("51678", ["51163"]),
]
REPLACE_FIPS = [
    ("02158", "02270"),
    ("46102", "46113"),
]

FIPS_TO_STATE = {v: k.lower() for k, v in STATE_TO_FIPS.items()}

# Fake fips to States

FAKE_FIPS_TO_STATES = {
    "90001":"al",
    "90002":"ak",
    "90004":"az",
    "90005":"ar",
    "90006":"ca",
    "90008":"co",
    "90009":"ct",
    "90010":"de",
    "90011":"dc",
    "90012":"fl",
    "90013":"ga",
    "90015":"hi",
    "90016":"id",
    "90017":"il",
    "90018":"in",
    "90019":"ia",
    "90020":"ks",
    "90021":"ky",
    "90022":"la",
    "90023":"me",
    "90024":"md",
    "90025":"ma",
    "90026":"mi",
    "90027":"mn",
    "90028":"ms",
    "90029":"mo",
    "90030":"mt",
    "90031":"ne",
    "90032":"nv",
    "90033":"nh",
    "90034":"nj",
    "90035":"nm",
    "90036":"ny",
    "90037":"nc",
    "90038":"nd",
    "90039":"oh",
    "90040":"ok",
    "90041":"or",
    "90042":"pa",
    "90044":"ri",
    "90045":"sc",
    "90046":"sd",
    "90047":"tn",
    "90048":"tx",
    "90049":"ut",
    "90050":"vt",
    "90051":"va",
    "90053":"wa",
    "90054":"wv",
    "90055":"wi",
    "90056":"wy"    
}


def fips_to_state(fips: str) -> str:
    """Wrapper that handles exceptions to the FIPS scheme in the JHU data.

    The two known exceptions to the FIPS encoding are documented in the JHU
    case data README.  All other county FIPS codes are mapped to state by
    taking the first two digits of the five digit, zero-padded county FIPS
    and applying FIPS_TO_STATE to map it to the two-letter postal
    abbreviation.

    Parameters
    ----------
    fips: str
        Five digit, zero padded county FIPS code

    Returns
    -------
    str
        Two-letter postal abbreviation, lower case.

    Raises
    ------
    KeyError
        Inputted FIPS code not recognized.
    """
    if fips == "70002":
        return FIPS_TO_STATE["25"]  # Dukes & Nantucket -> Massachusetts
    if fips == "70003":
        return FIPS_TO_STATE["29"]  # Kansas City -> Missouri
    # Fake fips -> states
    if fips[:2] == '90':
        return FAKE_FIPS_TO_STATES[fips]
    else:
        return FIPS_TO_STATE[fips[:2]]


def disburse(df: pd.DataFrame, pooled_fips: str, fips_list: list):
    """Disburse counts from POOLED_FIPS equally to the counties in FIPS_LIST.

    Parameters
    ----------
    df: pd.DataFrame
        Columns: fips, timestamp, new_counts, cumulative_counts, ...
    pooled_fips: str
        FIPS of county from which to disburse counts
    fips_list: list[str]
        FIPS of counties to which to disburse counts.

    Results
    -------
    pd.DataFrame
        Dataframe with same schema as df, with the counts disbursed.
    """
    COLS = ["new_counts", "cumulative_counts"]
    df = df.copy().sort_values(["fips", "timestamp"])
    for col in COLS:
        # Get values from the aggregated county:
        vals = df.loc[df["fips"] == pooled_fips, col].values / len(fips_list)
        for fips in fips_list:
            df.loc[df["fips"] == fips, col] += vals
    return df


def geo_map(df: pd.DataFrame, geo_res: str, map_df: pd.DataFrame, sensor: str):
    """
    Maps a DataFrame df, which contains data at the county resolution, and
    aggregate it to the geographic resolution geo_res.

    Parameters
    ----------
    df: pd.DataFrame
        Columns: fips, timestamp, new_counts, cumulative_counts, population ...
    geo_res: str
        Geographic resolution to which to aggregate.  Valid options:
        ('county', 'state', 'msa', 'hrr').
    map_df: pd.DataFrame
        Loaded from static file "fips_prop_pop.csv".

    Returns
    -------
    pd.DataFrame
        Columns: geo_id, timestamp, ...
    """
    VALID_GEO_RES = ("county", "state", "msa", "hrr")
    #It is not clear to calculate the proportion for unassigned cases/deaths
    PROP_SENSORS = ("incidence", "cumulative_prop")
    if geo_res not in VALID_GEO_RES:
        raise ValueError(f"geo_res must be one of {VALID_GEO_RES}")
 
    df_mega = df[df['fips'].astype(int) >= 90001].copy()
    df_mega['geo_id'] = df_mega['fips'].apply(fips_to_state)
    
    df = df[df['fips'].astype(int) < 90001].copy()
    
    if geo_res == "county":
        df["geo_id"] = df["fips"]
        if sensor not in PROP_SENSORS:
            df = df.append(df_mega)
    elif geo_res == "state":
        # Grab first two digits of fips
        # Map state fips to us postal code
        df["geo_id"] = df["fips"].apply(fips_to_state)
        # Add unassigned cases/deaths
        df = df.append(df_mega)
    elif geo_res in ("msa", "hrr"):
        # Disburse Dukes & Nantucket to individual counties
        df = disburse(df, DN_FIPS, DN_COUNTY_FIPS)
        # Disburse Kansas City to intersecting counties
        df = disburse(df, KC_FIPS, KC_COUNTY_FIPS)
        # Map "missing" secondary FIPS to those that are in our canonical set
        for fips, fips_list in SECONDARY_FIPS:
            df = disburse(df, fips, fips_list)
        # Our fips are outdated:
        #    https://www.census.gov/programs-surveys/
        #    geography/technical-documentation/county-changes.html
        for jhu_fips, our_fips in REPLACE_FIPS:
            df.loc[df["fips"] == jhu_fips, "fips"] = our_fips
        colname = "cbsa_id" if geo_res == "msa" else "hrrnum"
        map_df = map_df.loc[~pd.isnull(map_df[colname])].copy()
        map_df["geo_id"] = map_df[colname].astype(int)
        df["fips"] = df["fips"].astype(int)
        merged = pd.merge(df, map_df, on="fips")
        merged["cumulative_counts"] = merged["cumulative_counts"] * merged["pop_prop"]
        merged["new_counts"] = merged["new_counts"] * merged["pop_prop"]
        merged["population"] = merged["population"] * merged["pop_prop"]
        df = merged.drop(["zip", "pop_prop", "hrrnum", "cbsa_id"], axis=1)
        if sensor not in PROP_SENSORS:
            df = df.append(df_mega)
    df = df.drop("fips", axis=1)
    df = df.groupby(["geo_id", "timestamp"]).sum().reset_index()
    
    # Value would be negative for megacounties , which would not be considered in the main function
    df["incidence"] = df["new_counts"] / df["population"] * INCIDENCE_BASE
    df["cumulative_prop"] = df["cumulative_counts"] / df["population"] * INCIDENCE_BASE
    return df
