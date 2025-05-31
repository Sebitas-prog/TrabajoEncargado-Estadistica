import pandas as pd

def leer_excel_columnas(archivo):
    df = pd.read_excel(archivo)
    return df, df.columns.tolist()
