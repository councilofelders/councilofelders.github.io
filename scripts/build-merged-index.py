#!/usr/bin/env python3
"""
Build a unified search index for councilofelders.github.io.

Reads the existing inline page entries from index.html, fetches the meetups
README.md, parses all talk entries, merges them into a single array, and
writes the combined JSON back into the <script id="search-index"> tag.

Usage:
    python3 scripts/build-merged-index.py

    Updates index.html in place.  Run whenever new meetup content appears,
    then commit the result.
"""

import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, ".."))
INDEX_HTML = os.path.join(REPO_ROOT, "index.html")

MEETUPS_README_URL = (
    "https://raw.githubusercontent.com/councilofelders/meetups/master/README.md"
)

EVENT_NAMES: dict[int, str] = {
    1:  "Numerai Community Meetup London #1",
    2:  "Numerai Community Meetup New York City #2",
    3:  "Numerai Community Meetup Tokyo #3",
    4:  "Numerai Community Meetup Prague #4",
    5:  "Numerai Community Meetup Toronto #5",
    6:  "Numerai Community Meetup San Francisco #6",
    7:  "Numerai Community Meetup Frankfurt #7",
    8:  "Numerai Community Meetup Tokyo #8",
    9:  "Numerai Meetup Bangkok @ Superintelligence Summit #9",
    10: "Decentralized AI Day Seattle #10",
    11: "Decentralized AI Day Tokyo #11",
    12: "Decentralized AI Day Vienna #12",
    13: "Decentralized AI Day San Francisco #13",
    14: "Decentralized AI Day Vienna #14",
    15: "Decentralized AI Day Tokyo #15",
}

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May",     "06": "June",     "07": "July",   "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}

NON_TALK_PREFIXES = [
    r"Eventbrite",
    r"Meetup\b",
    r"Free Registration",
    r"Social Media",
    r"Other Links",
    r"Talks & Workshops",
    r"CrowdCent Workshop",
    r"YIEDL Workshop",
    r"Crunch Workshop",
    r"Allora Workshop",
    r"Description",
    r"Format",
    r"Audience",
    r"Led by",
    r"Goal",
    r"Sessions?\b",
    r"Why attend",
    r"\[Intro\]",
    r"\[Session",
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _format_date(date_str: str) -> str:
    parts = date_str.split("-")
    if len(parts) == 3:
        month_name = MONTH_NAMES.get(parts[1], parts[1])
        return f"{month_name} {parts[0]}"
    return date_str


def _city_slug(city: str) -> str:
    """Last meaningful segment of the city for short IDs."""
    # "Decentralized AI Day Tokyo 2026" -> "tokyo"
    # "San Francisco" -> "san-francisco"
    # "New York City" -> "new-york-city"
    parts = city.split()
    # Filter out generic words
    generic = {"decentralized", "ai", "day", "meetup", "community", "numerai", "@", "superintelligence", "summit"}
    meaningful = [p for p in parts if p.lower() not in generic]
    if meaningful:
        slug = "-".join(meaningful).lower()
    else:
        slug = "-".join(parts).lower()
    return slug


def _github_url(path: str) -> str:
    """Convert relative slides path to absolute GitHub URL."""
    if path.startswith("http"):
        return path
    path = path.lstrip("/")
    return f"https://github.com/councilofelders/meetups/blob/master/{path}"


def _talk_sort_key(raw: str) -> tuple:
    """Sort talks by embedded number then text."""
    m = re.search(r"(\d+)", raw)
    num = int(m.group(1)) if m else 999
    return (num, raw.lower())


def _detect_lang(label: str) -> str:
    label_upper = label.upper()
    if "JP" in label_upper and "EN" in label_upper:
        return "en&ja"
    elif "JP" in label_upper:
        return "ja"
    elif "EN" in label_upper:
        return "en"
    return "en"  # default


def _detect_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    return "other"


def _clean_title(raw: str) -> str:
    """Strip Talk #N - / Bonus Talk - prefix."""
    t = re.sub(r"^(?:Talk\s*#?\d+[a-z]?\s*[-–—]+\s*|Bonus Talk\s*[-–—]+\s*)", "", raw)
    return t.strip()


def _mk_id(date_str: str, city: str, idx: int) -> str:
    return f"meetup-{date_str}-{_city_slug(city)}-{idx:02d}"


# ---------------------------------------------------------------------------
# README parsing
# ---------------------------------------------------------------------------

def parse_meetup_entries(readme_text: str) -> list[dict]:
    entries: list[dict] = []
    sections = re.split(r"\n(?=##\s)", readme_text)

    for section in sections:
        section = section.strip()
        # Match "## Meetup #N - YYYY-MM-DD - City"
        header_match = re.match(r"##\s*Meetup\s*#(\d+)\s*[-–—]\s*(\d{4}-\d{2}-\d{2})\s*[-–—]\s*(.+)", section)
        if not header_match:
            continue

        event_num = int(header_match.group(1))
        event_date = header_match.group(2)
        city = header_match.group(3).strip()
        event_name = EVENT_NAMES.get(event_num, f"Meetup #{event_num} — {city}")

        lines = section.split("\n")
        talk_idx = 0

        for line in lines:
            line = line.strip()
            if not line.startswith("- **"):
                continue

            # Skip non-talk lines
            if re.match(r"^-\s*\*\*(?:__)?(?:" + "|".join(NON_TALK_PREFIXES) + r")(?:__)?\*\*", line):
                continue

            # Extract all link pairs: [**Label**](url)
            all_links = re.findall(r"\[\*\*(.+?)\*\*\]\((.+?)\)", line)
            # Also handle plain markdown links [Text](url)
            plain_links = re.findall(r"(?<!\[\*\*)\[([^\]]+)\]\(([^)]+)\)(?!\))", line)

            # Extract bold title
            title_match = re.search(r"\*\*(.+?)\*\*", line)
            if not title_match:
                continue
            raw_title = title_match.group(1)

            # ---- Skip purely informational lines ----
            # If there are no slide/video links and title is just a link label, skip
            slide_video_links = [
                (label, url) for label, url in all_links
                if "slide" in label.lower() or "video" in label.lower()
            ]

            # If it's a link-only item (no slide/video content)
            if not slide_video_links:
                # Keep only talks with "by" or permission markers
                if not re.search(r"\bby\b", line, re.IGNORECASE) and "No permission" not in line and "Contact Speaker" not in line:
                    continue

            talk_idx += 1

            # ---- Determine title ----
            # Check if bold text is a talk-number prefix
            talk_num_match = re.match(r'^(Talk\s*#?\d+[a-z]?|Bonus Talk)$', raw_title)
            if talk_num_match:
                # Real title follows the bold: "**Talk #N** - Actual Title by Speaker"
                after_bold = line[title_match.end():]
                title_extract = re.search(
                    r'^\s*[-–—]+\s*(.+?)\s+by\s+', after_bold
                )
                if title_extract:
                    title = title_extract.group(1).strip()
                else:
                    title = raw_title
            else:
                title = raw_title

            # ---- Detect special markers ----
            is_no_permission = "No permission" in line
            is_contact_speaker = bool(re.search(r"\*\*Contact Speaker\*\*", line))

            # ---- Extract speaker ----
            speaker = ""
            speaker_match = re.search(r"\bby\s+(.+?)(?:\s*[-–—]\s*(?:\[\*\*|$))", line)
            if speaker_match:
                speaker = speaker_match.group(1).strip()
            else:
                # Fallback: everything after "by" before a markdown link or end
                speaker_match2 = re.search(r"\bby\s+(.+?)(?:\s*\[\*\*|\s*\[|$)", line)
                if speaker_match2:
                    speaker = speaker_match2.group(1).strip()
            # Clean up speaker
            speaker = re.sub(r"\s+@\s+.*", "", speaker).strip()

            # ---- Build slides / videos maps ----
            slides: dict = {}
            videos: dict = {}
            has_slides = False
            has_video = False

            for label, url in slide_video_links:
                label_lower = label.lower()
                if "slide" in label_lower:
                    lang = _detect_lang(label)
                    slides[lang] = {"url": url, "language": lang}
                    has_slides = True
                elif "video" in label_lower:
                    lang = _detect_lang(label)
                    videos[lang] = {"url": url, "language": lang, "platform": _detect_platform(url)}
                    has_video = True

            # ---- Availability ----
            if is_no_permission:
                availability = "no-permission"
            elif has_slides and has_video:
                availability = "slides+video"
            elif has_slides:
                availability = "slides-only"
            elif has_video:
                availability = "video-only"
            else:
                availability = "talk-only"

            # ---- Snippet ----
            if availability == "no-permission":
                snippet = f"{title} — talk from {event_name}. Slides/video not shared."
            elif is_contact_speaker:
                snippet = f"{title} — talk from {event_name}. Contact speaker for details."
            elif availability in ("video-only", "talk-only"):
                snippet = f"{title} — talk from {event_name}, {_format_date(event_date)}"
            else:
                snippet = f"{title} — slides from {event_name}, {_format_date(event_date)}"

            # ---- Primary URL ----
            primary_url = ""
            if has_slides:
                first_slide = slides.get("en", next(iter(slides.values())))
                primary_url = _github_url(first_slide["url"])
            elif has_video:
                first_video = videos.get("en", next(iter(videos.values())))
                primary_url = first_video["url"]

            # ---- Convert relative slide URLs to absolute GitHub URLs ----
            for lang in slides:
                slides[lang]["url"] = _github_url(slides[lang]["url"])

            # ---- Subtitle ----
            sub_parts = []
            if speaker:
                sub_parts.append(speaker)
            sub_parts.append(event_name)
            sub_parts.append(_format_date(event_date))
            subtitle = " · ".join(sub_parts)

            # ---- Build entry ----
            entry: dict = {
                "id": _mk_id(event_date, city, talk_idx),
                "type": "resource",
                "tab": "resources",
                "title": title,
                "subtitle": subtitle,
                "snippet": snippet,
                "url": primary_url,
                "speaker": speaker,
                "event": event_name,
                "eventDate": event_date,
                "source": "meetup",
            }

            if slides:
                entry["slides"] = slides
            if videos:
                entry["videos"] = videos
            if availability:
                entry["availability"] = availability

            entries.append(entry)

    return entries


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    # 1. Read current inline JSON from index.html
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    script_pattern = r'(<script id="search-index"[^>]*>\s*)(\[.*?\])(\s*</script>)'
    match = re.search(script_pattern, html, re.DOTALL)
    if not match:
        print("ERROR: Could not find <script id='search-index'> in index.html", file=sys.stderr)
        sys.exit(1)

    page_entries = json.loads(match.group(2))
    # Only keep page entries (those not from meetup source)
    page_entries = [e for e in page_entries if e.get("source") != "meetup"]
    print(f"Found {len(page_entries)} existing page entries in inline JSON.")

    # 2. Fetch README.md
    print(f"Fetching {MEETUPS_README_URL} ...")
    try:
        with urllib.request.urlopen(MEETUPS_README_URL, timeout=30) as resp:
            readme = resp.read().decode("utf-8")
    except Exception as e:
        print(f"ERROR fetching README: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Parse meetup entries
    meetup_entries = parse_meetup_entries(readme)
    print(f"Parsed {len(meetup_entries)} meetup talk entries from README.")

    # 4. Merge: page entries first, then meetup entries (sorted by id)
    meetup_entries.sort(key=lambda e: e["id"])
    all_entries = page_entries + meetup_entries

    # 5. Replace inline JSON
    new_json = json.dumps(all_entries, indent=2, ensure_ascii=False)
    new_html = html[: match.start(2)] + new_json + html[match.end(2) :]

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Wrote {len(all_entries)} total entries to inline JSON in index.html.")
    print("Done.")


if __name__ == "__main__":
    main()
