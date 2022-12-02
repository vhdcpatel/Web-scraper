import sqlalchemy as db
from sqlalchemy import create_engine,inspect,MetaData
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# get tables and rows count in sqlite
def get_tables(db_name):
  try:
    engine = create_engine('sqlite:///'+db_name+'.db', echo=False)
    # insp = inspect(engine)  # create the inspector
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)


    tables  = list(meta_data.tables.keys())
    
    if len(tables) == 0:
      return None,None
    
    # tables = insp.get_table_names()
    num_rows = [] 
    for i in tables:
      temp2 ={} 
      temp_table = meta_data.tables[i]
      result = db.select([db.func.count()]).select_from(temp_table).scalar()
      num_rows.append(result)

    return tables,num_rows

  except Exception as e:
    print(e)
    return None,None


# delete all tables in sqlite
def delete_tables(db_name):
  try:
    engine = create_engine('sqlite:///'+db_name+'.db', echo=False)
    
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    tables  = list(meta_data.tables.keys())
    
    for i in tables:
      temp_table = meta_data.tables[i]
      temp_table.drop(engine)
    return "All tables deleted"

  except Exception as e:
    print(e)
    return "No tables found"


def main2():
  db_name = 'WS_data'
  try:
    tables,num_rows = get_tables(db_name)
    return tables,num_rows

  
  except Exception as e:
    print(e)




