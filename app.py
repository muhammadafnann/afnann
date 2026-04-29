import os
import sys
from flask import Flask, render_template, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.database import get_recent_metrics, get_recent_events, init_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def api_metrics():
    metrics = get_recent_metrics(20)
    return jsonify(metrics)

@app.route('/api/events')
def api_events():
    events = get_recent_events(20)
    return jsonify(events)

if __name__ == '__main__':
    init_db()
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
