import requests
import sqlite3
import os
import sys

URL = "http://localhost:8000"
DB_PATH = "backend/db.sqlite3"

def check_server():
    print(f"Checking access to {URL}...")
    try:
        response = requests.get(URL)
        print("✅ Server is reachable.")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend. Is 'run_backend.bat' running?")
        return False

def check_database():
    print(f"\nChecking database at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print("❌ Error: Database file 'db.sqlite3' not found in backend folder.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check for Equipment table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='equipment_equipment';")
        if cursor.fetchone():
            print("✅ Table 'equipment_equipment' exists.")
        else:
            print("❌ Error: Table 'equipment_equipment' MISSING. Migrations failed.")
            return False

        # Check for Dataset table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='equipment_dataset';")
        if cursor.fetchone():
            print("✅ Table 'equipment_dataset' exists.")
        else:
            print("❌ Error: Table 'equipment_dataset' MISSING. Migrations failed.")
            return False
            
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def check_api():
    print("\nChecking API endpoints...")
    try:
        # Try a simple GET request (Basic Auth required usually, but let's see response)
        # Using GET on login page is a safe "is it alive" check for Django
        response = requests.get(f"{URL}/admin/login/")
        if response.status_code == 200:
            print("✅ Admin Login verification successful (Server active).")
        else:
            print(f"⚠️ Server returned status {response.status_code} on admin page.")
    except Exception as e:
         print(f"❌ API Check Error: {e}")

if __name__ == "__main__":
    server_ok = check_server()
    if server_ok:
        db_ok = check_database()
        check_api()
        if server_ok and db_ok:
            print("\n🟢 BACKEND STATUS: HEALTHY")
            sys.exit(0)
    
    print("\n🔴 BACKEND STATUS: ISSUES DETECTED")
    sys.exit(1)
