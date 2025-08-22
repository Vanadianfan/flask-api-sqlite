# テンプレート

## テーブル作成

```bash
sqlite3 chat.db
```

```sqlite
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    source TEXT,
    likes INTEGER DEFAULT 0
);
```

```
.quit
```



## 実行コマンド

### 追加（例）

```bash
curl -X POST http://127.0.0.1:5000/api/messages \
     -H "Content-Type: application/json" \
     -d '{"message":"New Message","timestamp":"2025-08-20 23:30:00","source":"Slack","likes":5}'
```

### 一覧を見る

```bash
curl http://127.0.0.1:5000/api/messages
```

### 編集（例）

```bash
curl -X PUT http://127.0.0.1:5000/api/messages/1 \
     -H "Content-Type: application/json" \
     -d '{"likes":10}'
```

### 削除（例）

```
curl -X DELETE http://127.0.0.1:5000/api/messages/1
```
