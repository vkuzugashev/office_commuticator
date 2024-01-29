import sys
from flask import Flask, render_template
sys.path.insert(1, '..')
from models.model import db, table_calls

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

@app.route('/history')
def history():
    data = connection_bd()
    return render_template('history.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

