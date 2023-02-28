### How to do a Covidcast batch issue upload for chng:
##### When do to patches: One or more issues was never added due to an outage or previously-added issues needs to be corrected

<details>
  <summary> Step 0.5: Check for missing issue dates in database </summary>
Example Command: 

```
      select issue, max(time_value) from epimetric_full_v where source="chng" and `signal`="smoothed_outpatient_covid" and time_type="day" and geo_type="state" and issue>=20221201 group by issue; 
```

</details>

<details>
  <summary> Step 1: Change the indicator params to fit our needs </summary>

  + Insert note on File Structure here: 
   + Insert note on drop date here 
  
 We want to chnge the export directory and the indicator drop date. This will give us the data in the place that we want for the date that we need. 
  
Example params
  

```json
  {
  "common": {
    "export_dir": "[name-of-batch]/issue_[YYYYMMDD]/[data_source_name]",
  },
  "indicator": {
    "input_cache_dir": "./cache",
    "input_files": {
      "denom": null,
      "covid": null,
      "flu": null,
      "mixed": null,
      "flu_like": null,
      "covid_like": null
    },
    "start_date": null,
    "end_date": null,
    "drop_date": [Insert drop_date],
    "backfill_dir": "/common/backfill/chng",
    "backfill_merge_day": 0,
    "n_backfill_days": 60,
    "n_waiting_days": 3,
    "se": false,
    "parallel": false,
    "geos": ["state", "msa", "hrr", "county", "hhs", "nation"],
    "weekday": [true, false],
    "types": ["covid","cli","flu"],
    "wip_signal": "",
    "ftp_conn": {
      "host": "{}",
      "user": "{}",
      "pass": "{}",
      "port": "{}"
    }
  }
       
```

</details>

<details>
  <summary> Step 1.1: Make necessary directories and run the indicator </summary>
Make sure to run the indicator using the module instead of the runner: 

```
 env/bin/python -m delphi_changehc
```

</details>

  <details>
    <summary> Step 2: Convert to a diff-based issue </summary>
      We convert to diff-based issues in order to reduce the size of a data patch. If you are patching Cases or Deaths you shoul always perform this step. Otherwise it is user-discretion. You cn create these patches in two ways: using S3 or using the API. 
  
      versions.py
    
 </details>
<details>
  <summary> Step 3: Check Size  </summary>

</details>
<details>
  <summary> Step 4: Install  </summary>

</details>
 
</details>
