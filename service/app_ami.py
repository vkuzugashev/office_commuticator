import pika, os, time, json

from asterisk.ami import AMIClient, AutoReconnect

client = AMIClient(address='127.0.0.1', port=5038, timeout=60, encoding='ascii')
AutoReconnect(client)
future = client.login(username='admin',secret='ami-secret')

if future.response.is_error():
    raise Exception(str(future.response))

def event_listener(event,**kwargs):
    print('Event:',event.name)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='events')

    channel.basic_publish(exchange='',
                          routing_key='events',
                          body=json.dumps({'event': event.name, 'params': event.keys}))
    print(f"[x] Sent {event.name}")

    connection.close()


                        
#client.add_event_listener(
#    on_Newstate=event_listener,
#    white_list=re.compile('.*'),
#    ChannelStateDesc=re.compile('^Ring.*'),
#)

client.add_event_listener(event_listener, white_list=['DialBegin','DialEnd','Hangup'])

try:
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    client.logoff()
print('Exit')
