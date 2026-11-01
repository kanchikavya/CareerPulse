import os
import sys
import subprocess
from pathlib import Path

# Load environment
BASE_DIR = Path(__file__).resolve().parent
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

import pymysql

DB_NAME = os.environ.get('DB_NAME', 'job_portal_db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = int(os.environ.get('DB_PORT', 3306))


def setup_mysql():
    print("=" * 60)
    print("   CareerPulse - Automated Local MySQL Server Connector")
    print("=" * 60)
    print(f"Target Database: {DB_NAME}")
    print(f"Host: {DB_HOST}:{DB_PORT} | User: {DB_USER}")

    print("\n[1/4] Checking connection to local MySQL server...")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            charset='utf8mb4',
            connect_timeout=5,
        )
        print("  -> Connected successfully to local MySQL server!")
    except Exception as e:
        print(f"\n[!] Could not connect to MySQL on {DB_HOST}:{DB_PORT}.")
        print(f"    Error: {e}")
        print("\nTroubleshooting:")
        print("  1. If using XAMPP: Open XAMPP Control Panel and click 'Start' next to MySQL.")
        print("  2. If using MySQL Workbench / Server: Ensure the 'MySQL' service is started in Windows Services.")
        print("  3. If your MySQL has a password, update DB_PASSWORD in your .env file.")
        print("  4. Then run: python setup_mysql.py\n")
        return False

    print(f"\n[2/4] Ensuring database '{DB_NAME}' exists...")
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()
        print(f"  -> Database '{DB_NAME}' is ready!")
    except Exception as e:
        print(f"  [!] Failed to create database: {e}")
        return False

    print("\n[3/4] Enabling MySQL in .env (USE_MYSQL=True)...")
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        content = env_path.read_text(encoding='utf-8')
        if 'USE_MYSQL=False' in content:
            content = content.replace('USE_MYSQL=False', 'USE_MYSQL=True')
            env_path.write_text(content, encoding='utf-8')
            print("  -> Updated USE_MYSQL=True in .env")
        elif 'USE_MYSQL=True' in content:
            print("  -> USE_MYSQL is already True in .env")

    # Set environment variable in this process for subsequent commands
    os.environ['USE_MYSQL'] = 'True'

    print("\n[4/4] Running Django Migrations on MySQL...")
    try:
        res = subprocess.run([sys.executable, 'manage.py', 'migrate'], cwd=str(BASE_DIR), check=True)
        print("  -> All tables created in MySQL successfully!")
    except Exception as e:
        print(f"  [!] Migration error: {e}")
        return False

    print("\n[5/5] Seeding companies and jobs into MySQL...")
    try:
        subprocess.run([sys.executable, 'seed_all_companies.py'], cwd=str(BASE_DIR), check=True)
        print("  -> Seed data loaded into MySQL successfully!")
    except Exception as e:
        print(f"  [!] Seeding error: {e}")
        return False

    print("\n" + "=" * 60)
    print(" [SUCCESS] Project is now running on your local MySQL server!")
    print(f" Database: {DB_NAME} (viewable in phpMyAdmin / MySQL Workbench)")
    print("=" * 60)
    print("Run your server anytime with: python manage.py runserver\n")
    return True


if __name__ == '__main__':
    setup_mysql()
