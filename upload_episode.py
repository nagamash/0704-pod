#!/usr/bin/env python3
"""Upload today's episode files to maxblomqvist.se/pod/ via SFTP.

Uploads:
  - briefings/ai-briefing-YYYY-MM-DD.mp3
  - briefings/0704-cover-YYYY-MM-DD.png
  - feed.xml

Requires: pip install paramiko

Usage:
    python3 upload_episode.py                 # today
    python3 upload_episode.py 2026-05-05      # specific date
"""

import os
import sys
from datetime import date
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("Installing paramiko...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "paramiko", "-q"], check=True)
    import paramiko

POD_DIR    = Path(__file__).parent
BRIEF_DIR  = POD_DIR / "briefings"
REMOTE_DIR = "/customers/1/5/5/maxblomqvist.se/httpd.www/pod"

SFTP_HOST  = os.environ.get("SFTP_HOST", "ssh.maxblomqvist.se")
SFTP_PORT  = int(os.environ.get("SFTP_PORT", "22"))
SFTP_USER  = os.environ.get("SFTP_USER", "maxblomqvist.se")
SFTP_PASS  = os.environ.get("SFTP_PASS", "")


def load_env():
    env_path = POD_DIR.parent / "m4ix_001" / ".env"
    if not env_path.exists():
        env_path = POD_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def ensure_remote_dir(sftp, path: str):
    parts = path.split("/")
    current = ""
    for part in parts:
        if not part:
            current = "/"
            continue
        current = f"{current}/{part}" if current != "/" else f"/{part}"
        try:
            sftp.stat(current)
        except FileNotFoundError:
            sftp.mkdir(current)


def upload(target_date: date):
    date_str  = target_date.isoformat()
    mp3_path  = BRIEF_DIR / f"ai-briefing-{date_str}.mp3"
    cover_path = BRIEF_DIR / f"0704-cover-{date_str}.png"
    feed_path  = POD_DIR / "feed.xml"

    missing = [p for p in [mp3_path, feed_path] if not p.exists()]
    if missing:
        print(f"Missing required files: {[str(p) for p in missing]}")
        sys.exit(1)

    print(f"Connecting to {SFTP_HOST}...")
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        ensure_remote_dir(sftp, REMOTE_DIR)
        ensure_remote_dir(sftp, f"{REMOTE_DIR}/briefings")

        # Upload MP3
        remote_mp3 = f"{REMOTE_DIR}/briefings/{mp3_path.name}"
        print(f"Uploading {mp3_path.name} ({mp3_path.stat().st_size // 1024} KB)...")
        sftp.put(str(mp3_path), remote_mp3)

        # Upload cover if it exists
        if cover_path.exists():
            remote_cover = f"{REMOTE_DIR}/briefings/{cover_path.name}"
            print(f"Uploading {cover_path.name}...")
            sftp.put(str(cover_path), remote_cover)
        else:
            print(f"No cover found for {date_str}, skipping.")

        # Upload feed.xml
        print("Uploading feed.xml...")
        sftp.put(str(feed_path), f"{REMOTE_DIR}/feed.xml")

        print(f"\nDone. Feed live at: https://www.maxblomqvist.se/pod/feed.xml")

    finally:
        sftp.close()
        transport.close()


if __name__ == "__main__":
    load_env()

    SFTP_HOST = os.environ.get("SFTP_HOST", "ssh.maxblomqvist.se")
    SFTP_PORT = int(os.environ.get("SFTP_PORT", "22"))
    SFTP_USER = os.environ.get("SFTP_USER", "maxblomqvist.se")
    SFTP_PASS = os.environ.get("SFTP_PASS", "")

    if not SFTP_PASS:
        print("SFTP_PASS not set. Add it to m4ix_001/.env")
        sys.exit(1)

    args = sys.argv[1:]
    if args:
        try:
            target = date.fromisoformat(args[0])
        except ValueError:
            print(f"Invalid date: {args[0]}")
            sys.exit(1)
    else:
        target = date.today()

    upload(target)
