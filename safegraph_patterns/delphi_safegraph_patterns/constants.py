METRICS = [
        # signal_name, naics_code, wip
        ('bars_visit', 722410, False),
        ('restaurants_visit', 722511, False),
]
VERSIONS = [
    # release version, access dir, paths glob
    ("202106", "weekly-patterns-delivery-2020-12/release-2021-07/weekly", "patterns/*/*/*"),
]
SENSORS = [
        "num",
        "prop"
]
GEO_RESOLUTIONS = [
        "county",
        "hrr",
        "msa",
        "state",
        "hhs",
        "nation"
]
