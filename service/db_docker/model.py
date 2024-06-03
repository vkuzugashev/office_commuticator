from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PWD')
db_name = os.environ.get('DB_NAME')
print(f'mysql+pymysql://{user}:{password}@{db_host}/{db_name}')
db = create_engine(f'mysql+pymysql://{user}:{password}@{db_host}/{db_name}')

metadata = MetaData()

table_calls = Table('calls', metadata, 
    Column('id', Integer(),primary_key=True),
    Column('id_caller', String(200), nullable=False),
    Column('id_callee', String(200),  nullable=True),
    Column('client_id', String(200), nullable=True),
    Column('call_start', String(200), nullable=False),
    Column('call_end', String(200), nullable=True),
    Column('call_status', String(200), nullable=False)
)

if __name__ == '__main__':
    metadata.drop_all(db)
    metadata.create_all(db)
    print('Database schema created.')