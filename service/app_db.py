import pika, sys, os, json
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean


def callback(ch, method, properties, body):    
    print(f' [x] Received {body}')
    
    ch.basic_ack(delivery_tag = method.delivery_tag)
        
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='calls')   
    channel.basic_consume(queue='calls', auto_ack=False, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def callback(ch, method, properties, body):    
    print(f' [x] Received {body}')
    connection_bd(body)

def connection_bd(body):
    engine = create_engine("mysql+pymysql://root:1234567@localhost/call_center")
    conn = engine.connect()

    metadata = MetaData()

    blogs = Table('blog', metadata, 
        Column('id', Integer(),primary_key=True),
        Column('id_caller', String(200), nullable=False),
        Column('id_callee', String(200),  nullable=True),
        Column('call_start', String(200), nullable=False),
        Column('call_end', String(200), nullable=False),
        Column('call_status', String(200), nullable=False)
    )
    
    call = json.loads(body)
    print(call,'\r\n')
    
    ins = blogs.insert().values(
        id_caller = call['caller'],
        id_callee = call['callee'],
        call_start = call['start'],
        call_end = call['end'],
        call_status  = call['call_status']
    )

    print(ins)

    t = conn.begin()

    try:
        r = conn.execute(ins)
        t.commit()
        print("Транзакция завершена.")
    except:
        t.rollback()
        print("Транзакция не удалась.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

