from tools import tools

from google.cloud import bigquery

import datetime
import json
import os
import pandas as pd
import time
import urllib

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/raff/.ssh/ncssm-price-transparency-d58392a32442.json"

with open("config.json", "r") as f:
    config = json.load(f)
    
debug = False
debug_check = 13

nrows = None if debug else None

idx_start = debug_check   if debug else 0
idx_end   = debug_check+1 if debug else len(config["data"])
num_entries = idx_end - idx_start

if debug:
    print(f"Checking only {debug_check}")
    print(config["data"][debug_check])
else:
    print(f"Loading in all hospitals")
    
date_obtained = datetime.datetime.now().strftime("%Y-%m-%d")

for i in range(14, idx_end):
    entry = config["data"][i]
    
    identifier    = i
    hospital_name = entry["hospital_name"]
    filepath      = entry["data_url_local"] if "data_url_local" in entry else entry["data_url"]
    is_local      = "data_url_local" in entry
    filetype      = "csv"
    if "filetype" in entry:
        filetype = entry["filetype"]
    else:
        if filepath.endswith("json"):
            filetype = "json"
        elif filepath.endswith("xlsx"):
            filetype = "xlsx"
    
    fixed_start = entry["idx_column_fixed_start"]
    fixed_end = entry["idx_column_fixed_end"]
    
    transformed_columns = entry["transformed_columns"]
    
    skiprows      = entry["skiprows"]
    date_provided = entry["date_provided"]
    gross_charge_name   = entry["gross_charge_name"] if "gross_charge_name" in entry else None
    self_pay_name       = entry["self_pay_name"]     if "self_pay_name" in entry else None
    min_name = entry["min_name"] if "min_name" in entry else None
    max_name = entry["max_name"] if "min_name" in entry else None
    min_inpatient_name  = entry["min_inpatient_name"] if "min_inpatient_name" in entry else None
    max_inpatient_name  = entry["max_inpatient_name"] if "max_inpatient_name" in entry else None
    min_outpatient_name = entry["min_outpatient_name"] if "min_outpatient_name" in entry else None
    max_outpatient_name = entry["max_outpatient_name"] if "max_outpatient_name" in entry else None
    
    print(f"Processing {hospital_name} ({identifier} of {num_entries})")
    
    checkpoint_0   = time.time()

    df             = tools.read(filepath, skiprows, nrows, filetype = filetype, is_local = is_local)
    
    checkpoint_1   = time.time()
    time_taken    = "{:.2f}".format(checkpoint_1 - checkpoint_0)
    total_elapsed = "{:.2f}".format(checkpoint_1 - checkpoint_0)
    print(f"File read complete.  Shape: {df.shape}. Time taken: {time_taken}. Total time elapsed: {total_elapsed}")
    
    df_processed   = tools.process(df)
    
    checkpoint_2   = time.time()
    time_taken    = "{:.2f}".format(checkpoint_2 - checkpoint_1)
    total_elapsed = "{:.2f}".format(checkpoint_2 - checkpoint_0)
    print(f"Processing complete. Shape: {df_processed.shape}. Time taken: {time_taken}. Total time elapsed: {total_elapsed}")
    
    df_transformed = tools.transform(df_processed, fixed_start = fixed_start, fixed_end = fixed_end)    
    df_transformed.columns = transformed_columns
    
    checkpoint_3   = time.time()
    time_taken    = "{:.2f}".format(checkpoint_3 - checkpoint_2)
    total_elapsed = "{:.2f}".format(checkpoint_3 - checkpoint_0)
    print(f"Transform complete.  Shape: {df_transformed.shape}. Time taken: {time_taken}. Total time elapsed: {total_elapsed}")
    
    df_standardized = tools.standardize(df_transformed, 
                                        cols = ["code", "description", "payer", "cost"],
                                        id = identifier,
                                        date_obtained = date_obtained,
                                        date_provided = date_provided,
                                        hospital_name = hospital_name,
                                        gross_charge_name = gross_charge_name,
                                        self_pay_name = self_pay_name,
                                        min_name = min_name,
                                        max_name = max_name,
                                        min_inpatient_name = min_inpatient_name,
                                        max_inpatient_name = max_inpatient_name,
                                        min_outpatient_name = min_outpatient_name,
                                        max_outpatient_name = max_outpatient_name)
    
    checkpoint_4   = time.time()
    time_taken    = "{:.2f}".format(checkpoint_4 - checkpoint_3)
    total_elapsed = "{:.2f}".format(checkpoint_4 - checkpoint_0)
    print(f"Standardization complete. Shape: {df_standardized.shape}. Time taken: {time_taken}. Total time elapsed: {total_elapsed}")
    
    if not debug:
        job = tools.send_to_bigquery(df_standardized,
                                     destination_table = f"ncssm-price-transparency.hospital_data.hospital_{identifier}",
                                     cols_int64 = ["id"],
                                     cols_date  = ["date_obtained", "date_provided"])

        checkpoint_5   = time.time()
        time_taken    = "{:.2f}".format(checkpoint_5 - checkpoint_4)
        total_elapsed = "{:.2f}".format(checkpoint_5 - checkpoint_0)
        print(f"BQ load complete. Time taken: {time_taken}. Total time elapsed: {total_elapsed}")
    
    del df
    del df_processed
    del df_transformed
    del df_standardized