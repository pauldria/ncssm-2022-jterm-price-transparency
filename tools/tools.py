from google.cloud import bigquery

import datetime
import io
import pandas as pd
import requests

def _read_local(filepath, skiprows, nrows, filetype):
    if filetype == "csv":
        df = pd.read_csv(filepath, skiprows = skiprows, dtype = str, na_values = "", nrows = nrows, encoding = "latin1")
    elif filetype == "xlsx":
        df = pd.read_excel(filepath, skiprows = skiprows, dtype = str, na_values = "", nrows = nrows)

    return(df)

def _read_http(filepath, skiprows, nrows, filetype):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(filepath, headers = header)

    if filetype == "csv":
        df = pd.read_csv(io.StringIO(r.text), skiprows = skiprows, dtype = str, na_values = "", nrows = nrows, encoding = "latin1")
    elif filetype == "xlsx":
        df = pd.read_excel(io.StringIO(r.text), skiprows = skiprows, dtype = str, na_values = "", nrows = nrows)

    return(df)

def read(filepath, skiprows, nrows, filetype = "csv", is_local = False):
    if is_local:
        df = _read_local(filepath, skiprows, nrows, filetype)
    else:
        df = _read_http(filepath, skiprows, nrows, filetype)

    return(df)

def process(df):
    df.columns = [x.strip() for x in df.columns]
    df.fillna("", inplace = True)
    for c in df.columns:
        df[c] = df[c].map(str.strip)
    return(df)

def transform(df, fixed_start = 0, fixed_end = 4, melted_start = None, melted_end = None, var_name = "payer", value_name = "cost"):
    if melted_start is None:
        melted_start = fixed_end
    if melted_end is None:
        melted_end = len(df.columns)

    fixed_columns  = df.columns[fixed_start  : fixed_end]
    melted_columns = df.columns[melted_start : melted_end]

    df_transformed = df.melt(id_vars = fixed_columns, value_vars = melted_columns, var_name = var_name, value_name = value_name)

    return(df_transformed)

def standardize(df, cols, id, date_obtained, date_provided, hospital_name, gross_charge_name = "_ZZZ", self_pay_name = "_ZZZ", min_name = "_ZZZ", max_name = "_ZZZ", min_inpatient_name = "_ZZZ", max_inpatient_name = "_ZZZ", min_outpatient_name = "_ZZZ", max_outpatient_name = "_ZZZ"):
    df_standardized = df
    df_standardized["payer"] = ["_GROSS_CHARGE"   if x == gross_charge_name else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_SELF_PAY"       if x == self_pay_name     else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MINIMUM"  if x == min_name  else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MAXIMUM"  if x == max_name  else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MINIMUM_INPATIENT"  if x == min_inpatient_name  else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MAXIMUM_INPATIENT"  if x == max_inpatient_name  else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MINIMUM_OUTPATIENT" if x == min_outpatient_name else x for x in df_standardized["payer"]]
    df_standardized["payer"] = ["_MAXIMUM_OUTPATIENT" if x == max_outpatient_name else x for x in df_standardized["payer"]]

    df_standardized["id"] = id

    df_standardized["date_obtained"] = datetime.datetime.strptime(date_obtained, "%Y-%m-%d")
    df_standardized["date_provided"] = datetime.datetime.strptime(date_provided, "%Y-%m-%d")
    df_standardized["hospital_name"] = hospital_name

    if "code_type" not in cols:
        df_standardized["code_type"] = ""

    standard_cols = ["id", "date_obtained", "date_provided", "hospital_name", "code", "code_type", "description", "payer", "cost"]
    other_cols = [c for c in df_standardized.columns if c not in standard_cols]

    return(df_standardized[standard_cols + other_cols])

def send_to_bigquery(df, destination_table, cols_int64, cols_date):
    client = bigquery.Client()
    schema = []

    for c in df:
        bigquery_type = bigquery.enums.SqlTypeNames.STRING
        if c in ["id"]:
            bigquery_type = bigquery.enums.SqlTypeNames.INT64
        if c in ["date_obtained", "date_provided"]:
            bigquery_type = bigquery.enums.SqlTypeNames.DATE
        schema.append(bigquery.SchemaField(c, bigquery_type))

    job_config = bigquery.LoadJobConfig(
        schema            = schema,
        write_disposition = "WRITE_TRUNCATE",
    )

    job = client.load_table_from_dataframe(
        df,
        destination_table,
        job_config=job_config
    )

    return(job)
