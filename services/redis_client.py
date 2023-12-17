import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
client_info={'fio': 'Кузугашев Влдаимир Иванович', 'order': '777'}
r.set('79043744685', json.dumps(client_info))
cl = json.loads(r.get('79043744685'))
print(f'client_info={client_info}')
print(cl)
