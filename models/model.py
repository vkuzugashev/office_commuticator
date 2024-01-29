from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column

db = create_engine("mysql+pymysql://root:1234567@localhost/call_center")

metadata = MetaData()

table_calls = Table('calls', metadata, 
    Column('id', Integer(),primary_key=True),
    Column('id_caller', String(200), nullable=False),
    Column('id_callee', String(200),  nullable=True),
    Column('call_start', String(200), nullable=False),
    Column('call_end', String(200), nullable=True),
    Column('call_status', String(200), nullable=False)
)

if __name__ == '__main__':
    metadata.drop_all(db)
    metadata.create_all(db)
    print('Database schema created.')