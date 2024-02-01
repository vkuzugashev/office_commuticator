import sys
from flask import Flask, render_template, request
sys.path.insert(1, '.')
from models.model import db, table_calls
import math
import itertools

app = Flask(__name__)

@app.route('/')
def body():
    return render_template('body.html')

def connection_bd():
    conn = db.connect()
    s = table_calls.select()
    print(s)
    r = conn.execute(s)
    return r.fetchall()

def connection_bd2(fromdt, todt):
    conn = db.connect()
    s = table_calls.select().where((table_calls.c.call_start >= fromdt) & (table_calls.c.call_start <= todt))
    print(s)
    r = conn.execute(s)
    return r.fetchall()

   
def get_page(data, page_size, page_index):
    total_items = len(data)
    total_pages = (total_items + page_size - 1) // page_size
    start_index = (page_index - 1) * page_size
    end_index = page_index * page_size
    page_data = data[start_index:end_index]

    print(page_data)
    return page_data, total_pages

@app.route('/history', defaults={ 'page_index': 1, 'fromdt': '2024-01-01', 'todt': '2024-01-31' })
@app.route('/history/<fromdt>/<todt>/<int:page_index>', methods=['GET'])
def history(fromdt, todt, page_index):
    print(fromdt, todt, page_index)
    data = connection_bd2(fromdt, todt)
    page_data, total_pages = get_page(data, 1, page_index)
    return render_template('history.html', data=page_data, total_pages=total_pages, fromdt=fromdt, todt=todt, page_index=page_index)

if __name__ == '__main__':
    app.run(debug=True)

