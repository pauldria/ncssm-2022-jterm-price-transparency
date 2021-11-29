import datetime

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

def standardize(df, cols, id, date_obtained, date_provided, hospital_name, gross_charge_name, min_inpatient_name, max_inpatient_name, min_outpatient_name, max_outpatient_name):
    df_standardized = df.copy()[cols]
    df_standardized["payer"] = ["_GROSS_CHARGE"       if x == gross_charge_name   else x for x in df_standardized["payer"]]
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

    return(df_standardized[["id", "date_obtained", "date_provided", "hospital_name", "code", "code_type", "description", "payer", "cost"]])
