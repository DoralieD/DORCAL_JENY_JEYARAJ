from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

BACKEND_URL = "http://backend-service:5000/api/entries"

@app.route('/')
def index():
    try:
        response = requests.get(BACKEND_URL)
        entries = response.json()
    except:
        entries = []
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    content = request.form.get('content')
    if content:
        requests.post(BACKEND_URL, json={"content": content})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)