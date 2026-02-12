from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# This allows your HTML file to access this server
CORS(app) 

# --- Database Setup ---
# This runs once when you start the server to make sure the table exists
def init_db():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  message TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- API Routes ---

# 1. READ: Get all messages
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        conn = sqlite3.connect('guestbook.db')
        c = conn.cursor()
        # Get messages, newest first (ORDER BY id DESC)
        c.execute("SELECT name, message FROM messages ORDER BY id DESC")
        data = c.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. WRITE: Add a new message
@app.route('/api/sign', methods=['POST'])
def sign_guestbook():
    try:
        data = request.json
        name = data.get('name')
        message = data.get('message')

        if not name or not message:
            return jsonify({"error": "Missing name or message"}), 400

        conn = sqlite3.connect('guestbook.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Guestbook signed!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Server is running on http://localhost:5000")
    app.run(debug=True, port=5000)