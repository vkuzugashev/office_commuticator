from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def body():
    return render_template('body.html')

def connection_bd():
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

    s = blogs.select()

    r = conn.execute(s)

    return r.fetchall()

@app.route('/history')
def history():
    data = connection_bd()
#    data = [{'id': 1, 'caller': call['caller'], 'callee': call['callee'],
             #'start': call['start'], 'end': call['end'], 'call_status': call['call_status']}]
    return render_template('history.html', data=data)

if __name__ == '__main__':
    app.run(debug=False)

