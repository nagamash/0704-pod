#!/usr/bin/env python3
"""Generate a podcast RSS feed from the briefings folder.

Produces feed.xml in the Pod root. Run after each episode is added,
or wire into the daily task as step 12.

Usage:
    python3 gen_rss.py
"""

import os
import re
import glob
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from email.utils import format_datetime

POD_DIR    = Path(__file__).parent
BRIEF_DIR  = POD_DIR / "briefings"
FEED_PATH  = POD_DIR / "feed.xml"

# Public base URL where the briefings folder is served.
# Sir needs to point a static host at the briefings/ folder and set this.
BASE_URL       = "https://0704-pod.pages.dev"        # Cloudflare Pages — feed + cover art
B2_AUDIO_BASE  = "https://f003.backblazeb2.com/file/0704-pod"  # Backblaze B2 — MP3s

SHOW = {
    "title":       "0704",
    "description": (
        "0704 is a private daily AI intelligence briefing that starts producing itself "
        "at 07:04 every morning. It has one intended listener. You are not that listener.\n\n"
        "M4IX is a constructed identity: an AI alter-ego voiced through an Advanced "
        "Voice Clone, remixed into a distinct character with its own speaking cadence "
        "and rhythm. Trained on Max Blomqvist's editorial instincts and given a "
        "callsign. Each morning, M4IX briefs Max on what matters in AI and technology: "
        "the genuine developments, the policy shifts, the things that will matter in "
        "six months that most people are not yet paying attention to.\n\n"
        "This feed makes those briefings public. Nothing is changed for the audience. "
        "The briefing is addressed to one person. You are listening in."
    ),
    "author":      "Max Blomqvist",
    "email":       "hej@maxblomqvist.se",
    "language":    "en",
    "category":    "Technology",
    "explicit":    "false",
    "link":        "https://0704-pod.pages.dev",
}


def episode_date(filename: str) -> datetime | None:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if not m:
        return None
    try:
        d = datetime.strptime(m.group(1), "%Y-%m-%d")
        # Publish at 07:04 CET (UTC+2 in summer)
        return d.replace(hour=7, minute=4, tzinfo=timezone(timedelta(hours=2)))
    except ValueError:
        return None


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def episode_guid(path: Path) -> str:
    return hashlib.md5(path.name.encode()).hexdigest()


def cover_url(date_str: str) -> str:
    cover = BRIEF_DIR / f"0704-cover-{date_str}.png"
    if cover.exists():
        return f"{BASE_URL}/briefings/0704-cover-{date_str}.png"
    return f"{BASE_URL}/cover-art/0704_podcast_art_v2.png"


def xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_feed() -> str:
    mp3s = sorted(
        BRIEF_DIR.glob("ai-briefing-????-??-??.mp3"),
        key=lambda p: p.name,
        reverse=True,
    )

    items = []
    for mp3 in mp3s:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", mp3.name)
        if not m:
            continue
        date_str = m.group(1)
        pub_date = episode_date(mp3.name)
        if not pub_date:
            continue

        size     = file_size(mp3)
        guid     = episode_guid(mp3)
        mp3_url  = f"{B2_AUDIO_BASE}/{mp3.name}"
        art_url  = cover_url(date_str)

        # Read episode description from the script log if it exists
        script_md = BRIEF_DIR / f"ai-briefing-{date_str}.md"
        if script_md.exists():
            raw = script_md.read_text(encoding="utf-8")
            # Extract the Full Script section for the description
            m2 = re.search(r"## Full Script\s*\n+(.*?)(?:\n##|\Z)", raw, re.DOTALL)
            desc = f"0704 — {date_str[8:10]}.{date_str[5:7]}.{date_str[2:4]}\nSignal received."
        else:
            desc = f"0704 — {date_str}"

        items.append(f"""
    <item>
      <title>0704 — {date_str}</title>
      <description><![CDATA[{desc}]]></description>
      <pubDate>{format_datetime(pub_date)}</pubDate>
      <enclosure url="{xml_escape(mp3_url)}" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{guid}</guid>
      <itunes:title>0704 — {date_str}</itunes:title>
      <itunes:author>{xml_escape(SHOW["author"])}</itunes:author>
      <itunes:image href="{xml_escape(art_url)}"/>
      <itunes:duration>0</itunes:duration>
      <itunes:explicit>{SHOW["explicit"]}</itunes:explicit>
    </item>""")

    last_build = format_datetime(datetime.now(tz=timezone.utc))
    show_art   = f"{BASE_URL}/cover-art/0704_podcast_art_v2.png"

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{xml_escape(SHOW["title"])}</title>
    <description><![CDATA[{SHOW["description"]}]]></description>
    <link>{xml_escape(SHOW["link"])}</link>
    <language>{SHOW["language"]}</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <itunes:author>{xml_escape(SHOW["author"])}</itunes:author>
    <itunes:owner>
      <itunes:name>{xml_escape(SHOW["author"])}</itunes:name>
      <itunes:email>{xml_escape(SHOW["email"])}</itunes:email>
    </itunes:owner>
    <itunes:image href="{xml_escape(show_art)}"/>
    <itunes:category text="{xml_escape(SHOW["category"])}"/>
    <itunes:explicit>{SHOW["explicit"]}</itunes:explicit>
    {''.join(items)}
  </channel>
</rss>"""
    return feed


if __name__ == "__main__":
    feed = build_feed()
    FEED_PATH.write_text(feed, encoding="utf-8")
    mp3_count = len(list(BRIEF_DIR.glob("ai-briefing-????-??-??.mp3")))
    print(f"Feed written: {FEED_PATH}  ({mp3_count} episodes)")
    print(f"Point Spotify at: {BASE_URL}/feed.xml")
