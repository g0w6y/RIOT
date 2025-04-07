import os
import json
import socket
import joblib
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

logging.basicConfig(
    filename="detector.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

MODEL_FILE = "iot_anomaly_model.pkl"
DATASET_PATH = "dataset.csv"
LOG_SOURCE = "device_data.log"
ANOMALY_THRESHOLD = 0.85
MAX_LOG_ENTRIES = 500
PORT = 7000

app = Flask(__name__)
blocked_devices = set()

def get_host_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return {
        'hostname': hostname,
        'ip': local_ip,
        'port': PORT,
        'url': f"http://{local_ip}:{PORT}"
    }

class RIOTDetector:
    def __init__(self):
        self.supervised_model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, class_weight='balanced')
        self.unsupervised_model = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
        self.scaler = StandardScaler()
        self._train_model()

    def _train_model(self):
        df = pd.read_csv(DATASET_PATH)
        df = df.dropna()
        X = df.drop(columns=['label'])
        y = df['label'].apply(lambda x: 1 if x == 'attack' else 0)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        self.supervised_model.fit(X_train, y_train)
        self.unsupervised_model.fit(X_train)
        joblib.dump((self.supervised_model, self.unsupervised_model, self.scaler), MODEL_FILE)

def validate_log_entry(entry):
    required_fields = ['timestamp', 'device_id', 'ip_address', 'status']
    return all(field in entry for field in required_fields)

def read_all_logs(limit=None):
    logs = []
    if os.path.exists(LOG_SOURCE):
        with open(LOG_SOURCE, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if validate_log_entry(entry):
                        logs.append(entry)
                except json.JSONDecodeError:
                    continue
    return logs[-limit:] if limit else logs

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def analytics():
    try:
        logs = read_all_logs(MAX_LOG_ENTRIES)
        connected_devices = set()
        if os.path.exists("connected_devices.txt"):
            with open("connected_devices.txt", "r") as f:
                connected_devices = set(line.strip() for line in f if line.strip())
        
        metrics = {
            'totalDevices': len(connected_devices),
            'secureDevices': len([log for log in logs if log['status'] == 'NORMAL']),
            'anomalies': len([log for log in logs if log['status'] == 'ANOMALY']),
            'blockedDevices': len(blocked_devices),
            'hostInfo': get_host_info()
        }
        
        return jsonify({
            'metrics': metrics,
            'logs': logs[-20:],
            'blocked': list(blocked_devices)
        })
    except Exception as e:
        logging.error(f"Analytics error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/block/<device_id>', methods=['POST'])
def block_device(device_id):
    blocked_devices.add(device_id)
    logging.info(f"Device {device_id} blocked")
    return jsonify({'status': 'success'})

@app.route('/api/unblock/<device_id>', methods=['POST'])
def unblock_device(device_id):
    blocked_devices.discard(device_id)
    logging.info(f"Device {device_id} unblocked")
    return jsonify({'status': 'success'})

@app.route('/api/download_logs')
def download_logs():
    try:
        logs = read_all_logs()
        if not logs:
            return jsonify({'error': 'No logs found'}), 404
        
        import csv
        from io import StringIO
        fieldnames = set()
        for log in logs:
            fieldnames.update(log.keys())
        fieldnames = sorted(fieldnames)
        
        si = StringIO()
        writer = csv.DictWriter(si, fieldnames=fieldnames)
        writer.writeheader()
        for log in logs:
            writer.writerow({field: log.get(field, '') for field in fieldnames})
        
        return si.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=security_logs.csv'
        }
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/clear_logs', methods=['DELETE'])
def clear_logs():
    try:
        if os.path.exists(LOG_SOURCE):
            open(LOG_SOURCE, 'w').close()
        blocked_devices.clear()
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Clear logs error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    if not os.path.exists(LOG_SOURCE):
        open(LOG_SOURCE, 'w').close()
    
    host_info = get_host_info()
    print(f"\n=== Server Running ===")
    print(f"Local URL: {host_info['url']}")
    print(f"Network IP: {host_info['ip']}")
    print(f"Hostname: {host_info['hostname']}")
    print(f"Port: {host_info['port']}\n")
    
    riot = RIOTDetector()
    app.run(host='0.0.0.0', port=PORT)
