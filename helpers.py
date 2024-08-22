import arcpy
import pandas as pd
import numpy as np

def get_pandas(table_url, fields = None):
    if fields is None:
        fields = get_table_fields(table_url)

    df = pd.DataFrame(data = arcpy.da.SearchCursor(table_url.valueAsText, fields), columns = fields)
    df = df.drop(["Shape__Area", "Shape__Length", "Shape"], axis=1, errors = "ignore")
    
    return df

def get_table_fields(table_url):
    return [f.name for f in arcpy.ListFields(table_url.valueAsText)]

def get_value_table_fields(value_table):
    if value_table.values is not None:
        return [str(field) for field in value_table.values[0]]
    else:
        return [None for i, col in enumerate(value_table.columns)]

def write_table(output_table, output_url):
    output_fields = output_table.columns.values.tolist()
    output_np = np.rec.fromrecords(output_table, names = output_fields)
    arcpy.da.NumPyArrayToTable(output_np, output_url.valueAsText)
