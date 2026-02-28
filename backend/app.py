from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'mysql-service'),
                user='root',
                password=os.getenv('DB_PASSWORD', 'rootpassword'),
                database='journaldb'
            )
            return conn
        except:
            time.sleep(5)
            retries -= 1
    return None

def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS entries (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        conn.commit()
        conn.close()

init_db()

@app.route('/api/entries', methods=['GET'])
def get_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM entries ORDER BY date DESC')
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    data = request.json
    content = data.get('content')
    if content:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (content) VALUES (%s)', (content,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Entrée ajoutée"}), 201
    return jsonify({"error": "Contenu vide"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)