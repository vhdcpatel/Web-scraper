import pandas as pd 
from sqlalchemy import create_engine

def download_data(db_name,table_name):
  
  engine = create_engine('sqlite:///'+db_name+'.db', echo=False)
  df = pd.read_sql_table(table_name,engine)
  return df

def main3(table_name):
  db_name = 'WS_data'

  df = download_data(db_name,table_name)
  return df