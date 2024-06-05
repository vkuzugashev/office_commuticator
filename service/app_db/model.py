import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, DateTime

load_dotenv()

db_url = os.environ.get('DB_URL')
db = create_engine(db_url, echo=True)

metadata = MetaData()

table_calls = Table('calls', metadata, 
    Column('id', Integer, primary_key=True, autoincrement='auto'),
    Column('caller', String(20), nullable=False),
    Column('callee', String(20),  nullable=False),
    Column('caller_id', String(100), nullable=True),
    Column('callee_id', String(100), nullable=True),
    Column('call_start', DateTime, nullable=False),
    Column('call_end', DateTime, nullable=True),
    Column('call_status', String(50), nullable=True),
    Column('record_file', String(255), nullable=True)
)

if __name__ == '__main__':
    metadata.drop_all(db)
    metadata.create_all(db)
    print('Database schema created.')
