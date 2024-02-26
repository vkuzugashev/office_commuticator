import pika, sys, os, redis, json, re, requests, websockets, asyncio, random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

rabbit_host = os.environ.get('RABBIT_HOST')
redis_host = os.environ.get('REDIS_HOST')

def uniqueid_to_timestamp(uniqueid):
    ts = int(re.search('\d{10}', uniqueid)[0])
    return ts

def get_redis_client():
    pool = redis.ConnectionPool(host=redis_host, port=6379)
    return redis.Redis(connection_pool=pool)

def redis_get(key):
    r = get_redis_client()
    value = r.get(key)
    print(f' [x] Get from redis: {key} -> {value}\r\n')
    return value
    
def redis_set(key, value):
    r = get_redis_client()
    r.set(key, value, ex=3600)
    print(f' [x] Stored in redis: {key} -> {value}\r\n')
    
def get_client_id(msisdn):
    response = requests.get(f'http://127.0.0.1:8000/clients/{msisdn}')
    content = response.content
    if response.status_code == 200:
        data = json.loads(content)
        client_id = (data['client_id'])
        print('Got client_id: ', data['client_id'])
        return client_id
    elif response.status_code == 404:
        return None

def dial_begin(uniqueid, caller, callee, start, call_status):
    client_id = get_client_id(caller)
    call = {'uniqueid': uniqueid, 'start': start, 'end': None, 'caller': caller, 'callee': callee, 'client_id': client_id, 'call_status': call_status}    
    id_callee = {'callee': callee, 'client_id': client_id}   
    redis_set(uniqueid, json.dumps(call))

def dial_end(uniqueid, call_status):
    str_call = redis_get(uniqueid)
    call = json.loads(str_call)
    call['call_status'] = call_status
    redis_set(uniqueid, json.dumps(call))
   
def hangup(uniqueid, end):
    str_call = redis_get(uniqueid)
    call = json.loads(str_call)
    if call['call_status'] == 'ANSWER':
        call['end'] = end
    store_to_queue(call)

def store_to_queue(call,**kwargs):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host, port=5672))
    channel = connection.channel()
    
    channel.queue_declare(queue='calls')

    channel.basic_publish(exchange='',
                          routing_key='calls',
                          body=json.dumps(call))
    print(f' [x] Store call to queue: {call}')
    
def set_call(key):
    r = get_redis_client()
    r.setex(key, 60)
    
def event_parse_and_route(body):
    
    event = json.loads(body)
    print(type(event),'\r\n')
    
    if event['event'] == 'DialBegin':
        # начало дозвона
        uniqueid = event['params']['Uniqueid']        
        caller = event['params']['CallerIDNum']
        callee = event['params']['DestCallerIDNum']
        # todo сделать конвертацию в timestamp с милисекундами, сейчас мы их отбрасываем
        ts = uniqueid_to_timestamp(uniqueid)
        start = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')     
        call_status = event['params']['ChannelStateDesc']
        dial_begin(uniqueid, caller, callee, start, call_status)
        
    elif event['event'] == 'DialEnd' and event['params']['DialStatus'] in ['CANCEL','BUSY','NOANSWER','ANSWER']:
        # Конец дозвона
        uniqueid = event['params']['Uniqueid']
        call_status = event['params']['DialStatus']
        dial_end(uniqueid, call_status)
                
    elif event['event'] == 'Hangup':
        # Конц вызова абонент повешал трубку
        uniqueid = event['params']['Linkedid']
        end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
        hangup(uniqueid, end)
    
    else:
        print(f'Unknow event: {body}\r\n')

def callback(ch, method, properties, body):    
    print(f' [x] Received {body}')
    event_parse_and_route(body)
        
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
    channel = connection.channel()
    channel.queue_declare(queue='events')   
    channel.basic_consume(queue='events', auto_ack=True, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
