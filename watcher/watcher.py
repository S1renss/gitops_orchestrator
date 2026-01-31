import time
from git import Repo
import sqlite3
import os

REPO_URL = "https://github.com/S1renss/app.git"
REPO_PATH = "/tmp/repo"
PROJECT_NAME = "myapp"

def init_repo():
    if not os.path.exists(REPO_PATH):
        print("[Watcher] Cloning repository...")
        return Repo.clone_from(REPO_URL, REPO_PATH)
    return Repo(REPO_PATH)

def get_last_commit(repo):
    return repo.head.commit.hexsha

def save_deploy(commit_hash):
    conn = sqlite3.connect("orchestrator.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO deploys (project, commit_hash, status) VALUES (?, ?, ?, ?)",
        (PROJECT_NAME, commit_hash, "pending")
    )

    conn.commit()
    conn.close()

def watcher_loop():
    repo = init_repo()
    last_commit = get_last_commit(repo)

    print("[Watcher] Started")

    while True:
        repo.remotes.origin.pull()
        new_commit = get_last_commit(repo)

        if new_commit != last_commit:
            print(f"[Watcher] New commit detected: {new_commit}")
            save_deploy(new_commit)
            last_commit = new_commit

            time.sleep(10)

if __name__ == "__main__":
    watcher_loop()