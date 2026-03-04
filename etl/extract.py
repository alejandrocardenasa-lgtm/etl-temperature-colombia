import pandas as pd

def extract(file_path):

    #Cargar csv
    df = pd.read_csv(file_path, sep=",", quotechar='"')
    df.columns = df.columns.str.strip()
    
    return df