import os
import shutil
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

DATABASE_DIR = 'databases'
BACKUP_DIR = 'backups'

# Gui thong bao qua email
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# Backup cac tap tin database va gui thong bao
def backup_databases():
    # Tao thu muc sao luu
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(backup_folder)

    # Backup file
    backup_files = []
    for file in os.listdir(DATABASE_DIR):
        if file.endswith(('.sql', '.sqlite3')):
            src_path = os.path.join(DATABASE_DIR, file)
            dst_path = os.path.join(backup_folder, file)
            shutil.copy2(src_path, dst_path)
            backup_files.append(file)

    # Gui email
    subject = "Database backup"
    body = f"Backup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    body += f"file da backup:\n{'\n'.join(backup_files)}" if backup_files else f"ko tim thay file database {DATABASE_DIR}"
    send_email(subject, body)

schedule.every().day.at("00:00").do(backup_databases)

if __name__ == "__main__":
    print("Khoi dong lich trinh backup database...")
    while True:
        schedule.run_pending()
        time.sleep(60)