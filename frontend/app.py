from flask import Flask, render_template, request, redirect
import os, requests

app = Flask(__name__)

BACKEND_URL = "http://backend-service:5000/api/entries"

@app.route('/')
def index():
    try:
        r = requests.get(BACKEND_URL)
        e = r.json()
    except:
        e = []
    return render_template('index.html', entries=e)

@app.route('/add', methods=['POST'])
def add_entry():
    c = request.form.get('content')
    if c:
        requests.post(BACKEND_URL, json={"content": c})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)