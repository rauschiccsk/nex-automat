"""
Read n8n projects and workflow assignments
"""
import sqlite3
import sys
from pathlib import Path


def read_n8n_projects(db_path):
    """Read projects and workflow assignments"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Read projects
        cursor.execute("SELECT id, name, type, createdAt FROM project")
        projects = cursor.fetchall()

        print("=" * 80)
        print(f"n8n PROJECTS ({len(projects)} total):")
        print("=" * 80)

        for proj_id, name, proj_type, created in projects:
            print(f"\n📁 {name} (Type: {proj_type})")
            print(f"   ID: {proj_id}")
            print(f"   Created: {created}")

            # Find workflows in this project
            cursor.execute("""
                SELECT w.id, w.name, w.active 
                FROM workflow_entity w
                JOIN shared_workflow sw ON w.id = sw.workflowId
                WHERE sw.projectId = ?
                ORDER BY w.name
            """, (proj_id,))
            workflows = cursor.fetchall()

            if workflows:
                print(f"   Workflows: {len(workflows)}")
                for wf_id, wf_name, active in workflows:
                    status = "🟢" if active else "🔴"
                    print(f"     {status} {wf_name}")
            else:
                print("   Workflows: 0")

        # Find workflows WITHOUT project assignment
        cursor.execute("""
            SELECT w.id, w.name, w.active 
            FROM workflow_entity w
            WHERE w.id NOT IN (SELECT workflowId FROM shared_workflow)
            ORDER BY w.name
        """)
        orphans = cursor.fetchall()

        if orphans:
            print(f"\n{'=' * 80}")
            print(f"⚠️  WORKFLOWS BEZ PROJEKTU ({len(orphans)} total):")
            print("=" * 80)
            for wf_id, name, active in orphans:
                status = "🟢" if active else "🔴"
                print(f"  {status} {name} (ID: {wf_id})")

        # Check user project relations
        cursor.execute("""
            SELECT u.email, p.name as project_name, pr.role
            FROM project_relation pr
            JOIN user u ON pr.userId = u.id
            JOIN project p ON pr.projectId = p.id
        """)
        user_projects = cursor.fetchall()

        if user_projects:
            print(f"\n{'=' * 80}")
            print("USER PROJECT ASSIGNMENTS:")
            print("=" * 80)
            for email, proj_name, role in user_projects:
                print(f"  {email} → {proj_name} ({role})")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Chyba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    db_path = Path(r"C:\Users\ZelenePC\.n8n\database.sqlite")

    if not db_path.exists():
        print(f"❌ Databáza nenájdená: {db_path}")
        sys.exit(1)

    print(f"📂 Databáza: {db_path}\n")
    read_n8n_projects(db_path)