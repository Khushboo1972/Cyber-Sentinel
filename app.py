# app.py
from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'cybersecurity_events.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM data")
    incidents = cur.fetchall()
    return render_template('index.html', incidents=incidents)


@app.route('/incident/<event_id>')
def incident_detail(event_id):
    db = get_db()
    incident = db.execute("SELECT * FROM data WHERE EventID = ?", (event_id,)).fetchone()
    response = db.execute("SELECT * FROM response WHERE EventID = ?", (event_id,)).fetchone()
    if incident is None:
        abort(404)
    return render_template('detail.html', incident=incident, response=response)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

