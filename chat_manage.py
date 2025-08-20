import sqlite3
from flask import Flask, jsonify, request
a = 10

app = Flask(__name__)
DB_PATH = "chat.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 全メッセージ一覧
@app.route('/api/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM chat_messages").fetchall()
    conn.close()
    return jsonify([dict(msg) for msg in messages])

# メッセージ追加
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_messages (message, timestamp, source, likes) VALUES (?, ?, ?, ?)",
        (data['message'], data['timestamp'], data['source'], data.get('likes', 0))
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, **data}), 201

# メッセージ編集：id経由
@app.route('/api/messages/<int:msg_id>', methods=['PUT'])
def update_message(msg_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    msg = cur.execute("SELECT * FROM chat_messages WHERE id = ?", (msg_id,)).fetchone()
    if msg is None:
        conn.close()
        return jsonify({"error": "Message not found"}), 404

    message = data.get("message", msg["message"])
    timestamp = data.get("timestamp", msg["timestamp"])
    source = data.get("source", msg["source"])
    likes = data.get("likes", msg["likes"])

    cur.execute(
        "UPDATE chat_messages SET message = ?, timestamp = ?, source = ?, likes = ? WHERE id = ?",
        (message, timestamp, source, likes, msg_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"id": msg_id, "message": message, "timestamp": timestamp, "source": source, "likes": likes})

# 削除：id経由
@app.route('/api/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    conn = get_db_connection()
    cur = conn.cursor()

    msg = cur.execute("SELECT * FROM chat_messages WHERE id = ?", (msg_id,)).fetchone()
    if msg is None:
        conn.close()
        return jsonify({"error": "Message not found"}), 404

    cur.execute("DELETE FROM chat_messages WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return "", 204

if __name__ == '__main__':
    app.run(debug=True)