import pandas as pd
def load_csv(file):
    df = pd.read_csv(file)
    return df
def get_summary(df):
    numeric_cols= df.select_dtypes(include="number").columns.tolist()
    text_cols= df.select_dtypes(include="object").columns.tolist()
    summary ={
        "total_rows":len(df),
        "total_columns":len(df.columns),
        "numeric_columns": numeric_cols,
        "text_columns": text_cols,
        "missing_values": df.isnull().sum().sum(),
    }
    return summary
def get_statistics(df):
    numeric_df= df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe().T.round(2)
def get_column_options(df):
    numeric_cols=df.select_dtypes(include="number").columns.tolist()
    text_cols=df.select_dtypes(include="object").columns.tolist()
    return numeric_cols, text_cols
def get_groupby_summary(df, group_col, value_col):
    result = df.groupby(group_col)[value_col].sum().reset_index()
    result.columns =[group_col, f"Total_{value_col}"]
    return result.sort_values(f"Total_{value_col}", ascending=False)
