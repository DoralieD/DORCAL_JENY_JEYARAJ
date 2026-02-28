from flask import Flask, request, jsonify
import mysql.connector, os, time

app = Flask(__name__)

def get_db_connection():
    r = 5
    while r > 0:
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
            r -= 1
    return None

def init_db():
    c = get_db_connection()
    if c:
        cursor = c.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS entries (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        c.commit()
        c.close()

init_db()

@app.route('/api/entries', methods=['GET'])
def get_entries():
    c = get_db_connection()
    cursor = c.cursor(dictionary=True)
    cursor.execute('SELECT * FROM entries ORDER BY date DESC')
    res = cursor.fetchall()
    c.close()
    return jsonify(res)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    d = request.json
    content = d.get('content')
    if content:
        c = get_db_connection()
        cursor = c.cursor()
        cursor.execute('INSERT INTO entries (content) VALUES (%s)', (content,))
        c.commit()
        c.close()
        return jsonify({"message": "Entrée ajoutée"}), 201
    return jsonify({"error": "Contenu vide"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)