#!/usr/bin/env python3
"""Yandex Mail helper via IMAP/XOAUTH2 and SMTP"""
import imaplib
import smtplib
import ssl
import email
import json
import sys
import re
import os
import base64
from email.header import decode_header
from email.message import EmailMessage
from html.parser import HTMLParser

TOKEN_FILE = os.path.expanduser("~/.openclaw/yax-token.json")

def load_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)["access_token"]

def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)

def get_mail():
    token = load_token()
    email_addr = "davydov.e.v@yandex.ru"
    auth_string = f"user={email_addr}\x01auth=Bearer {token}\x01\x01"
    mail = imaplib.IMAP4_SSL("imap.yandex.ru", 993)
    mail.authenticate("XOAUTH2", lambda x: auth_string.encode())
    return mail

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
        if tag in ('p', 'div', 'br'):
            self.result.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.result.append(data)

def strip_html(text):
    try:
        parser = TextExtractor()
        parser.feed(text)
        text = ''.join(parser.result)
    except Exception:
        text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()[:3000]

def get_body(msg):
    for part in msg.walk():
        ct = part.get_content_type()
        if ct in ("text/plain", "text/html"):
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload:
                text = payload.decode(charset, errors="replace")
                if ct == "text/html":
                    text = strip_html(text)
                return text[:2000]
    return "(no text body)"

def get_attachments(msg):
    """Возвращает список вложений: [(filename, content, content_type)]"""
    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = decode_str(part.get_filename())
            if filename:
                payload = part.get_payload(decode=True)
                if payload:
                    ct = part.get_content_type()
                    attachments.append((filename, payload, ct))
    return attachments

def cmd_attachments(uid, folder="INBOX"):
    """Показать вложения письма"""
    mail = get_mail()
    status, _ = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return
    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    attachments = get_attachments(msg)
    if not attachments:
        print("📎 Нет вложений")
        return
    print(f"📎 Вложения ({len(attachments)}):")
    for i, (filename, content, ct) in enumerate(attachments):
        size = len(content) / 1024
        print(f"  [{i}] {filename} ({size:.1f} KB)")

def cmd_download(uid, attachment_name, folder="INBOX", output_dir="."):
    """Скачать конкретное вложение"""
    mail = get_mail()
    status, _ = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return
    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    attachments = get_attachments(msg)
    for filename, content, ct in attachments:
        if filename == attachment_name:
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(content)
            print(f"✅ Saved: {filepath}")
            return
    print(f"❌ Attachment '{attachment_name}' not found")

def cmd_download_all(uid, folder="INBOX", output_dir="./attachments"):
    """Скачать все вложения письма"""
    mail = get_mail()
    status, _ = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return
    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    attachments = get_attachments(msg)
    if not attachments:
        print("📎 Нет вложений")
        return
    os.makedirs(output_dir, exist_ok=True)
    for filename, content, ct in attachments:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        print(f"✅ {filepath}")

def cmd_list(folder, limit=10):
    mail = get_mail()
    status, data = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder} ({data})")
        return
    _, msgs = mail.search(None, "ALL")
    ids = msgs[0].split()
    total = len(ids)
    print(f"📬 {folder}: {total} messages (showing last {limit})")
    for uid in ids[-limit:]:
        _, msg_data = mail.fetch(uid, "(ENVELOPE RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subj = decode_str(msg["Subject"]) or "(no subject)"
        date = msg["Date"]
        sender = decode_str(msg["From"])
        if len(sender) > 40:
            sender = sender[:37] + "..."
        print(f"  [{uid.decode()}] {date[:16]} | {sender}")
        print(f"         {subj[:60]}")

def cmd_read(uid, folder="INBOX"):
    mail = get_mail()
    status, _ = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return
    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    subj = decode_str(msg["Subject"])
    date = msg["Date"]
    sender = decode_str(msg["From"])
    to = decode_str(msg.get("To", ""))
    body = get_body(msg)
    print(f"From: {sender}")
    print(f"To: {to}")
    print(f"Date: {date}")
    print(f"Subject: {subj}")
    print(f"\n{body}")

def cmd_delete(uid, folder="INBOX"):
    mail = get_mail()
    status, _ = mail.select(folder)
    if status != "OK":
        print(f"❌ Cannot open folder: {folder}")
        return
    try:
        mail.store(uid.encode(), "+FLAGS", "\\Deleted")
        mail.expunge()
        print(f"✅ Deleted message {uid}")
    except Exception as e:
        print(f"❌ Delete failed: {e}")

def cmd_send(to, subject, body):
    token = load_token()
    email_from = "davydov.e.v@yandex.ru"
    auth_string = f"user={email_from}\x01auth=Bearer {token}\x01\x01"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP("smtp.yandex.ru", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            code, _ = server.docmd("AUTH", f"XOAUTH2 {auth_bytes}")
            if code != 235:
                print(f"❌ SMTP auth failed: {code}")
                return
            server.send_message(msg)
        print(f"✅ Письмо отправлено → {to}")
    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")


def cmd_folders():
    mail = get_mail()
    _, data = mail.list()
    folder_map = {
        "&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-": "Отправленные",
        "&BBgEQQRFBD4ENARPBEkEOAQ1-": "Рассылки",
        "&BCEEPwQwBDw-": "Спам",
        "&BCMENAQwBDsENQQ9BD0ESwQ1-": "Корзина",
        "&BCcENQRABD0EPgQyBDgEOgQ4-": "Черновики",
        "INBOX": "INBOX",
    }
    for item in data:
        line = item.decode()
        found = False
        for k, v in folder_map.items():
            if k in line:
                prefix = "📤" if "Sent" in v or "Отправл" in v else "📥" if v == "INBOX" else "📁"
                print(f"  {prefix} {v}")
                found = True
                break
        if not found and "Archive" in line:
            print(f"  📦 Archive")
        elif not found and "INBOX" in line:
            print(f"  📥 INBOX")
        elif not found:
            parts = line.split('"|"')
            if len(parts) > 1:
                name = parts[-1].strip().strip('"').strip()
                if name and name not in ("INBOX",):
                    print(f"  📁 {name}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    folder = "INBOX"
    limit = 10

    if cmd == "list":
        folder = sys.argv[2] if len(sys.argv) > 2 else "INBOX"
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        cmd_list(folder, limit)
    elif cmd == "read":
        if len(sys.argv) < 3:
            print("Usage: mail.py read <uid> [folder]")
        else:
            uid = sys.argv[2]
            if len(sys.argv) > 3:
                folder = sys.argv[3]
            cmd_read(uid, folder)
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Usage: mail.py delete <uid> [folder]")
        else:
            uid = sys.argv[2]
            if len(sys.argv) > 3:
                folder = sys.argv[3]
            cmd_delete(uid, folder)
    elif cmd == "folders":
        cmd_folders()
    elif cmd == "send":
        if len(sys.argv) < 4:
            print("Usage: mail.py send <to> <subject> <body>")
        else:
            to = sys.argv[2]
            subject = sys.argv[3]
            body = sys.argv[4] if len(sys.argv) > 4 else ""
            cmd_send(to, subject, body)
    elif cmd == "attachments":
        if len(sys.argv) < 3:
            print("Usage: mail.py attachments <uid> [folder]")
        else:
            uid = sys.argv[2]
            folder = sys.argv[3] if len(sys.argv) > 3 else "INBOX"
            cmd_attachments(uid, folder)
    elif cmd == "download":
        if len(sys.argv) < 4:
            print("Usage: mail.py download <uid> <attachment_name> [folder] [output_dir]")
        else:
            uid = sys.argv[2]
            attachment_name = sys.argv[3]
            folder = sys.argv[4] if len(sys.argv) > 4 else "INBOX"
            output_dir = sys.argv[5] if len(sys.argv) > 5 else "."
            cmd_download(uid, attachment_name, folder, output_dir)
    elif cmd == "download_all":
        if len(sys.argv) < 3:
            print("Usage: mail.py download_all <uid> [folder] [output_dir]")
        else:
            uid = sys.argv[2]
            folder = sys.argv[3] if len(sys.argv) > 3 else "INBOX"
            output_dir = sys.argv[4] if len(sys.argv) > 4 else "./attachments"
            cmd_download_all(uid, folder, output_dir)
    else:
        print("Usage: mail.py [list|read|delete|folders|send|attachments|download|download_all]")
