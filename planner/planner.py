import sqlite3
import os
from datatime import datatime

PLANS_DIR = "/tmp/deploy_plans"

def get_pending_deploys():
    conn = sqlite3.connect("orchestrator.db")
    cur = conn.cursor()

    cur.execute("SELECT id, project, commit_hash FROM deploys WHERE status = 'pending'")
    rows = cur.fetchall()

    conn.close()
    return rows

def create_deploy_plan(deploy_id, project, commit_hash):
    if not os.path.exists(PLANS_DIR):
        os.mkdir(PLANS_DIR)

    plan_path = os.path.join(PLANS_DIR, f"deploy_{deploy_id}.txt")

    steps = [
        "checkout code",
        "generate manifests",
        "validate manifests",
        "apply manifests",
        "health check",
        "finalize"
    ]

    with open(plan_path, "w") as f:
        for step in steps:
            f.write(f"{datatime.now()} | {step}\n")

    print(f"[Planner] Plan created for deploy {deploy_id}")
    return plan_path

def planner_loop():
    while True:
        pending = get_pending_deploys()
        for deploy in pending:
            deploy_id, project, commit_hash = deploy
            create_deploy_plan(deploy_id, project, commit_hash)

            # Обновляем статус в базе, чтобы не обрабатывать повторно
            conn = sqlite3.connect("orchestrator.db")
            cur = conn.cursor()
            cur.execute("UPDATE deploys SET status = 'planned' WHERE id = ?", (deploy_id,))
            conn.commit()
            conn.close()
        # Проверка каждые 10 секунд
        import time
        time.sleep(10)

if __name__ == "__main__":
    print("[Planner] Started")
    planner_loop()