import sqlite3

def init_db():
    conn = sqlite3.connect("orchestrator.db")
    cur = conn.cursor()

    # Таблица деплоев
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deploys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT,
        commit_hash TEXT,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Таблица логов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deploy_id INTEGER,
        step TEXT,
        message TEXT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
