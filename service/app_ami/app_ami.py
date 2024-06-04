import logging
import pika, os, time, json
from dotenv import load_dotenv
from asterisk.ami import AMIClient, AutoReconnect

load_dotenv()

log_level = os.environ.get('LOG_LEVEL', 'INFO')
asterisk_host = os.environ.get('ASTERISK_HOST', 'localhost')
asterisk_port = int(os.environ.get('ASTERISK_PORT', '5038'))
asterisk_user = os.environ.get('ASTERISK_USER')
asterisk_pwd = os.environ.get('ASTERISK_PWD')
rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
rabbit_port = int(os.environ.get('RABBIT_PORT', '5672'))

logging.basicConfig(level=log_level)
logger = logging.getLogger('app_ami')

def event_listener(event,**kwargs):
    logger.info('Event:',event)    
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host, port=rabbit_port))
    channel = connection.channel()
    channel.queue_declare(queue='events')
    channel.basic_publish(exchange='',
                          routing_key='events',
                          body=json.dumps({'event': event.name, 'params': event.keys}))
    logger.info(f"[x] Sent Event: {event}")
    connection.close()

def run():
    logger.info('app_ami starting ...')
    
    client = AMIClient(address=asterisk_host, port=asterisk_port, timeout=180, encoding='ascii')
    AutoReconnect(client)    
    client.add_event_listener(event_listener, white_list=['DialBegin','DialEnd','Hangup'])
    
    future = client.login(username=asterisk_user,secret=asterisk_pwd)
    if future.response.is_error():
        raise Exception(str(future.response))
    
    logger.info('app_ami started.')
    
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        client.logoff()
    
    logger.info('app_ami stopped')

if __name__ == '__main__':
    run()
