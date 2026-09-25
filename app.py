import os

from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)


@app.get('/')
def home():
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ChaosArmor Python Demo</title>
    <style>body{font:18px system-ui;background:#101b2e;color:#eef4ff;
    max-width:760px;margin:12vh auto;padding:24px}a{color:#7de0bd}
    section{border:1px solid #3b506d;padding:32px;border-radius:16px}</style>
    </head><body><section><p>CHAOSARMOR · PYTHON DEMO</p>
    <h1>Flask app is running.</h1><p>A sample web app for the Jenkins build pipeline.</p>
    <p><a href="/health">Health check</a> · <a href="/api/info">Application info</a></p>
    </section></body></html>'''


@app.get('/health')
def health():
    return jsonify(status='ok')


@app.get('/api/info')
def info():
    return jsonify(name='chaosarmor-python-demo', version='0.1.0', framework='Flask')


if __name__ == '__main__':
    serve(app, host=os.getenv('HOST', '127.0.0.1'), port=int(os.getenv('PORT', '5010')))
