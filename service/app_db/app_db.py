import logging, pika, sys, os, json
from datetime import datetime
from model import db, table_calls
from dotenv import load_dotenv

load_dotenv()

log_level = os.environ.get('LOG_LEVEL', 'INFO')
rabbit_host = os.environ.get('RABBIT_HOST')
rabbit_port = int(os.environ.get('RABBIT_PORT', '5672'))

logging.basicConfig(level=log_level)
logger = logging.getLogger('app_db')
        
def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
    channel = connection.channel()
    channel.queue_declare(queue='calls')   
    channel.basic_consume(queue='calls', auto_ack=False, on_message_callback=callback)
    logger.info('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def callback(ch, method, properties, body):    
    logger.info(f'[x] Received {body}')
    result = store_to_db(body)
    if result:
        ch.basic_ack(delivery_tag = method.delivery_tag)

def store_to_db(body):
    conn = db.connect()   
    call = json.loads(body)
   
    ins = table_calls.insert().values(
        id_caller = call['caller'],
        id_callee = call['callee'],
        client_id = call['client_id'],
        call_start = call['start'],
        call_end = call['end'],
        call_status  = call['call_status']
    )

    tran = conn.begin()

    try:
        conn.execute(ins)
        tran.commit()
        logger.info(f'Call success stored to db, call: {call}')
        return True
    except:
        tran.rollback()
        logger.info(f'Call fail store to db, call: {call}')
        return False


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

