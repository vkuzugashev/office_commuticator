import pika, sys, os, json
from datetime import datetime
sys.path.insert(1, '.')
from service.db_docker.model import db, table_calls

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
    conn = db.connect()
   
    call = json.loads(body)
    print(call,'\r\n')
    
    ins = table_calls.insert().values(
        id_caller = call['caller'],
        id_callee = call['callee'],
        call_start = call['start'],
        call_end = call['end'],
        call_status  = call['call_status']
    )

    print(ins)

    tran = conn.begin()

    try:
        conn.execute(ins)
        tran.commit()
        print("Транзакция завершена.")
    except:
        tran.rollback()
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

