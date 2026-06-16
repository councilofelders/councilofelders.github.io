#!/usr/bin/env python3
"""
Build a cross-source search index JSON file (v2) from the councilofelders/meetups repo.

v2 schema: per-talk entries (not per-PDF). Same talk with EN/JP slides -> one entry
with multiple slides entries. Video links extracted from README. "No permission"
handling. YIEDL event support.

Usage:
    python3 scripts/build-cross-source-index.py <meetups_root> <output_path>

    <meetups_root> : path to a clone of councilofelders/meetups (or test fixture)
    <output_path>  : where to write cross-source-index.json
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from collections import OrderedDict

# ---------------------------------------------------------------------------
# Mapping from directory name city-slug to canonical city name & event name
# ---------------------------------------------------------------------------
EVENT_INFO: dict[str, dict] = {
    "2022-07-16-london": {
        "event": "Numerai Community Meetup London #1",
        "city": "London",
    },
    "2022-09-24-nyc": {
        "event": "Numerai Community Meetup New York City #2",
        "city": "New York City",
    },
    "2023-04-08-tokyo": {
        "event": "Numerai Community Meetup Tokyo #3",
        "city": "Tokyo",
    },
    "2023-07-08-prague": {
        "event": "Numerai Community Meetup Prague #4",
        "city": "Prague",
    },
    "2023-10-14-toronto": {
        "event": "Numerai Community Meetup Toronto #5",
        "city": "Toronto",
    },
    "2024-01-16-san-francisco": {
        "event": "Numerai Community Meetup San Francisco #6",
        "city": "San Francisco",
    },
    "2024-04-27-frankfurt": {
        "event": "Numerai Community Meetup Frankfurt #7",
        "city": "Frankfurt",
    },
    "2024-07-20-tokyo": {
        "event": "Numerai Community Meetup Tokyo #8",
        "city": "Tokyo",
    },
    "2024-11-11-bangkok": {
        "event": "Numerai Meetup Bangkok @ Superintelligence Summit #9",
        "city": "Bangkok",
    },
    "2025-03-29-seattle": {
        "event": "Decentralized AI Day Seattle #10",
        "city": "Seattle",
    },
    "2025-05-17-tokyo": {
        "event": "Decentralized AI Day Tokyo #11",
        "city": "Tokyo",
    },
    "2025-09-20-vienna": {
        "event": "Decentralized AI Day Vienna #12",
        "city": "Vienna",
    },
    "2026-01-27-san-francisco": {
        "event": "Decentralized AI Day San Francisco #13",
        "city": "San Francisco",
    },
    "2026-03-21-vienna": {
        "event": "Decentralized AI Day Vienna #14",
        "city": "Vienna",
    },
    "2026-05-30-tokyo": {
        "event": "Decentralized AI Day Tokyo #15",
        "city": "Tokyo",
    },
}


def _parse_event_dir_name(dirname: str) -> tuple[str, str]:
    """Parse a directory name like '2026-05-30-tokyo' into (date_str, city_slug)."""
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-([a-z-]+)$", dirname)
    if not match:
        return dirname, dirname
    return match.group(1), match.group(2)


def _parse_pdf_filename(filename: str) -> dict | None:
    """
    Parse a PDF filename into its components.

    Pattern: YYYY-MM-DD-city-NN-talk-title-by-speaker[-lang].pdf
    Some files have no `-by-speaker` part.
    Language suffix is optional: `-en`, `-jp`, `-en-jp`, etc.

    Returns dict or None if filename doesn't match expected pattern.
    """
    base = filename[:-4] if filename.endswith(".pdf") else filename

    # 1. Strip language suffix (always at end before .pdf)
    lang = ""
    lang_match = re.search(r"-(en|jp|en-jp|jp-en|english|japanese)$", base)
    if lang_match:
        lang = lang_match.group(1)
        base = base[: lang_match.start()]

    # 2. Parse structured parts
    parts_match = re.match(
        r"(\d{4}-\d{2}-\d{2})-([a-z][a-z-]*?)-(\d{1,2}[a-z]?)[-_](.+)",
        base,
    )
    if not parts_match:
        return None

    date_str = parts_match.group(1)
    city_slug = parts_match.group(2)
    talk_num = parts_match.group(3)
    after_num = parts_match.group(4)

    # 3. Separate talk title from speaker (everything after last `-by-`)
    speaker = ""
    talk_title = after_num
    by_match = re.search(r"-by-", after_num)
    if by_match:
        talk_title = after_num[: by_match.start()]
        speaker = after_num[by_match.start() + 4:]
        speaker = speaker.strip()

    # Clean title: replace hyphens with spaces, title-case
    talk_title = talk_title.strip().replace("-", " ").title()

    return {
        "talk_num": talk_num,
        "talk_title": talk_title,
        "speaker": speaker.strip(),
        "language": lang,
        "filename": filename,
    }


def _make_snippet(title: str, event_name: str, date_str: str, city: str,
                  availability: str) -> str:
    """Build a short human-readable snippet."""
    month_names = {
        "01": "January", "02": "February", "03": "March", "04": "April",
        "05": "May", "06": "June", "07": "July", "08": "August",
        "09": "September", "10": "October", "11": "November", "12": "December",
    }
    try:
        ym = date_str.split("-")
        month_name = month_names.get(ym[1], ym[1])
        year = ym[0]
        date_fmt = f"{month_name} {year}"
    except (IndexError, ValueError):
        date_fmt = date_str

    if availability == "no-permission":
        return f"{title} — talk from {event_name}, {date_fmt}. Slides/video not shared."
    elif availability in ("video-only", "talk-only", "not-shared"):
        return f"{title} — talk from {event_name}, {date_fmt}"
    return f"{title} — slides from {event_name}, {date_fmt}"


def _make_tags(title: str, city: str, date_str: str, speaker: str,
               event_name: str) -> list[str]:
    """Generate searchable tags."""
    tags = []

    for word in title.lower().split():
        cleaned = re.sub(r"[^a-z0-9]", "", word)
        if cleaned and len(cleaned) > 1:
            tags.append(cleaned)

    tags.append(city.lower().replace(" ", "-"))

    try:
        ym = date_str.split("-")
        month_names_short = {
            "01": "jan", "02": "feb", "03": "mar", "04": "apr",
            "05": "may", "06": "jun", "07": "jul", "08": "aug",
            "09": "sep", "10": "oct", "11": "nov", "12": "dec",
        }
        tags.append(f"{month_names_short.get(ym[1], ym[1])}-{ym[0]}")
    except (IndexError, ValueError):
        pass

    if speaker:
        speaker_parts = speaker.split()
        if speaker_parts:
            tags.append(speaker_parts[-1].lower())

    num_match = re.search(r"#(\d+)", event_name)
    if num_match:
        tags.append(f"meetup-{num_match.group(1)}")

    return sorted(set(tags))


def _normalize_talk_num(raw: str) -> str:
    """Normalize a talk number for README lookup.
    Strip leading zeros, handle letter suffixes like '04a' -> '4a'.
    """
    digits_part = re.sub(r"[a-z].*$", "", raw)
    suffix_part = raw[len(digits_part):]
    if digits_part.isdigit():
        normalized = str(int(digits_part))
    else:
        normalized = digits_part
    return normalized + suffix_part


def _detect_video_url_platform(url: str) -> str:
    """Detect platform from video URL."""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "vimeo.com" in url:
        return "vimeo"
    return "other"


def _compute_availability(slides: dict | None, videos: dict | None,
                          no_permission: bool, not_shared: bool) -> str:
    """Compute availability enum from slides/videos presence and special markers."""
    if no_permission:
        return "no-permission"
    if not_shared:
        return "not-shared"
    has_slides = slides is not None and len(slides) > 0
    has_videos = videos is not None and len(videos) > 0
    if has_slides and has_videos:
        return "slides+video"
    elif has_slides:
        return "slides-only"
    elif has_videos:
        return "video-only"
    return "talk-only"


def _compute_primary_url(slides: dict | None, videos: dict | None) -> tuple:
    """
    Heuristic: prefer EN slides, else any slides, else EN video, else any video.
    Returns (primaryUrl, primaryKind, primaryLanguage).
    """
    if slides:
        # Prefer EN
        if "en" in slides:
            return slides["en"]["url"], "slides", "en"
        # Any slides
        first_lang = next(iter(slides))
        return slides[first_lang]["url"], "slides", first_lang

    if videos:
        if "en" in videos:
            return videos["en"]["url"], "video", "en"
        first_lang = next(iter(videos))
        return videos[first_lang]["url"], "video", first_lang

    return None, None, "en"


def _pdf_lang_to_code(lang: str) -> str:
    """Map PDF filename language suffix to a standard code."""
    mapping = {
        "en": "en",
        "jp": "ja",
        "english": "en",
        "japanese": "ja",
        "en-jp": "en&ja",
        "jp-en": "en&ja",
    }
    return mapping.get(lang, lang or "")


def _readme_lang_to_code(label: str) -> str:
    """Map a README language label (from 'Slides (EN)', 'Video (JP)', etc.) to a standard code."""
    if not label:
        return "en"  # default
    mapping = {
        "EN": "en",
        "JP": "ja",
        "EN & JP": "en&ja",
        "JP + EN": "en&ja",
    }
    return mapping.get(label.upper(), label.lower() or "en")


# Callable-type entries for non-standard talks
WELCOME_PATTERNS = re.compile(
    r"^\s*\*\*(Welcoming Remarks|Quick Update(?: on Numerai Meetups)?)\*\*",
    re.IGNORECASE,
)

# Fireside chat / Closing remarks / Bonus talk patterns
SPECIAL_TALK_PATTERNS = re.compile(
    r"^\s*\*\*(The Numerai Community Fireside Chat|Closing Remarks|"
    r"Bonus Talk\b.*?)\*\*",
    re.IGNORECASE,
)

# YIEDL patterns for Vienna #14 and beyond
YIEDL_INTRO_PATTERN = re.compile(r"^\s*\*\*\[Intro\]\s+(.+?)\s*[—–-]+\s*\d+\s*min\b", re.IGNORECASE)
YIEDL_SESSION_PATTERN = re.compile(
    r"^\s*\*\*\[Session\s+(\d+)\]\s+(.+?)\s*[—–-]+\s*\d+\s*min\b", re.IGNORECASE
)
YIEDL_SESSION_NOMIN = re.compile(
    r"^\s*\*\*\[Session\s+(\d+)\]\s+(.+?)\s*[—–]+\s*[^-—–]+$", re.IGNORECASE
)


def build_index(meetups_root: str) -> list[dict]:
    """
    Scan the meetups repo and build the v2 cross-source search index.

    Returns a list of v2 TalkEntry dicts ready for JSON serialization,
    sorted by id.
    """
    slides_dir = os.path.join(meetups_root, "slides")
    readme_path = os.path.join(meetups_root, "README.md")

    if not os.path.isdir(slides_dir):
        print(f"Error: slides directory not found at {slides_dir}", file=sys.stderr)
        sys.exit(1)

    # Parse README - build a detailed per-talk structure
    readme_talks: dict[str, list[dict]] = {}
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            readme_content = fh.read()
        _parse_readme_v2(readme_content, readme_talks)

    # Collect ALL PDF files on disk, indexed by (dirname, talk_num, lang)
    pdf_map: dict[tuple[str, str, str], dict] = {}

    event_dirs = sorted(
        d for d in os.listdir(slides_dir)
        if os.path.isdir(os.path.join(slides_dir, d))
    )

    for dirname in event_dirs:
        dir_path = os.path.join(slides_dir, dirname)
        for fname in sorted(os.listdir(dir_path)):
            if not fname.endswith(".pdf"):
                continue
            parsed = _parse_pdf_filename(fname)
            if parsed is None:
                print(f"Warning: could not parse {dirname}/{fname}", file=sys.stderr)
                continue
            key = (dirname, parsed["talk_num"], parsed["language"])
            pdf_map[key] = parsed

    # Build entries - one per "talk" (unique talk_num per event dir)
    entries = []
    seen_ids: set[str] = set()

    for dirname in event_dirs:
        date_str, city_slug = _parse_event_dir_name(dirname)
        event_info = EVENT_INFO.get(dirname, {
            "event": f"Meetup — {dirname}",
            "city": dirname.split("-", 3)[-1] if "-" in dirname else dirname,
        })
        event_name = event_info["event"]
        city = event_info["city"]

        # Get event number
        event_num = 0
        num_match = re.search(r"#(\d+)", event_name)
        if num_match:
            event_num = int(num_match.group(1))

        # Collect all talk numbers for this event from README and PDFs
        talk_numbers: set[str] = set()

        # From README
        if dirname in readme_talks:
            for rt in readme_talks[dirname]:
                talk_numbers.add(rt["talk_num"])

        # From PDFs on disk
        for (ed, tn, _) in pdf_map:
            if ed == dirname:
                talk_numbers.add(tn)

        # Sort talk numbers in a natural order
        def _sort_key(tn: str) -> tuple:
            digits = re.sub(r"[a-z]", "", tn)
            letter = tn[len(digits):] if digits else tn
            return (int(digits) if digits.isdigit() else 0, letter)

        for talk_num in sorted(talk_numbers, key=_sort_key):
            # Gather README metadata for this talk
            readme_info = None
            if dirname in readme_talks:
                for rt in readme_talks[dirname]:
                    if rt["talk_num"] == talk_num:
                        readme_info = rt
                        break

            # Gather PDFs for this talk across all languages
            pdfs_for_talk = []
            for (ed, tn, lang), pdata in pdf_map.items():
                if ed == dirname and tn == talk_num:
                    pdfs_for_talk.append(pdata)

            # Build the entry
            entry = _build_talk_entry(
                dirname=dirname,
                date_str=date_str,
                city=city,
                event_name=event_name,
                event_num=event_num,
                talk_num=talk_num,
                readme_info=readme_info,
                pdfs=pdfs_for_talk,
                seen_ids=seen_ids,
            )
            if entry:
                entries.append(entry)

    # Sort by id for deterministic output
    entries.sort(key=lambda e: e["id"])
    return entries


def _build_talk_entry(
    dirname: str,
    date_str: str,
    city: str,
    event_name: str,
    event_num: int,
    talk_num: str,
    readme_info: dict | None,
    pdfs: list[dict],
    seen_ids: set[str],
) -> dict | None:
    """Build a single v2 TalkEntry dict."""
    # Determine title
    title = readme_info["title"] if (readme_info and readme_info.get("title") and readme_info["title"] != "n/a") else ""
    if not title and pdfs:
        title = pdfs[0]["talk_title"]

    speaker = readme_info["speaker"] if (readme_info and readme_info.get("speaker") and readme_info["speaker"] != "n/a") else ""
    if not speaker and pdfs:
        speaker = pdfs[0]["speaker"]

    # Detect special markers
    is_no_permission = readme_info and readme_info.get("no_permission", False)
    is_not_shared = readme_info and readme_info.get("not_shared", False)
    is_fireside = readme_info and readme_info.get("is_fireside", False)
    is_closing = readme_info and readme_info.get("is_closing", False)
    is_bonus = readme_info and readme_info.get("is_bonus", False)

    # Build slides map
    slides: dict | None = {}
    for pdf in pdfs:
        lang_code = _pdf_lang_to_code(pdf["language"])
        if not lang_code:
            lang_code = "en"
        # Determine language label from README if available
        slides[lang_code] = {
            "url": (
                f"https://github.com/councilofelders/meetups/blob/master/slides/"
                f"{dirname}/{pdf['filename']}"
            ),
            "filename": pdf["filename"],
            "language": lang_code,
        }

    if not slides:
        slides = None

    # Build videos map
    videos: dict | None = {}
    if readme_info and readme_info.get("videos"):
        for v in readme_info["videos"]:
            lang_code = _readme_lang_to_code(v.get("lang", ""))
            videos[lang_code] = {
                "url": v["url"],
                "platform": _detect_video_url_platform(v["url"]),
                "language": lang_code,
            }

    if not videos or len(videos) == 0:
        videos = None

    # Compute availability
    availability = _compute_availability(
        slides, videos, is_no_permission, is_not_shared
    )

    # Handle fireside/closing/bonus: if they only have video, set video-only
    if availability == "talk-only" and videos and not slides:
        availability = "video-only"

    # Primary language: try to determine
    primary_lang = "en"
    if readme_info and readme_info.get("language"):
        primary_lang = _readme_lang_to_code(readme_info["language"])

    # Build primaryUrl
    primary_url, primary_kind, primary_lang = _compute_primary_url(slides, videos)

    # For no-permission and not-shared, primaryUrl must be null
    if availability in ("no-permission", "not-shared"):
        primary_url = None
        primary_kind = None

    # Build snippet
    snippet = ""
    if readme_info and readme_info.get("snippet"):
        snippet = readme_info["snippet"]
    if not snippet:
        snippet = _make_snippet(title, event_name, date_str, city, availability)

    # Build ID: meetup-{YYYY-MM-DD}-{city}-{talkNum}
    id_base = talk_num.zfill(2)
    entry_id = f"meetup-{date_str}-{city.lower().replace(' ', '-')}-{id_base}"

    # Ensure unique
    if entry_id in seen_ids:
        suffix = 2
        while f"{entry_id}-{suffix}" in seen_ids:
            suffix += 1
        entry_id = f"{entry_id}-{suffix}"
    seen_ids.add(entry_id)

    # Tags
    tags = _make_tags(title, city, date_str, speaker, event_name)

    entry: dict = OrderedDict()
    entry["id"] = entry_id
    entry["type"] = "meetup-slide"
    entry["title"] = title
    entry["speaker"] = speaker
    entry["event"] = event_name
    entry["eventNumber"] = event_num
    entry["eventDate"] = date_str
    entry["city"] = city
    entry["language"] = primary_lang
    entry["tags"] = tags
    entry["snippet"] = snippet
    entry["availability"] = availability

    if slides is not None:
        entry["slides"] = slides
    if videos is not None:
        entry["videos"] = videos
    if primary_url is not None:
        entry["primaryUrl"] = primary_url
        entry["primaryKind"] = primary_kind
        entry["primaryLanguage"] = primary_lang
    else:
        entry["primaryUrl"] = None
        entry["primaryKind"] = None
        entry["primaryLanguage"] = primary_lang

    return entry


def _parse_readme_v2(content: str, meta: dict[str, list[dict]]) -> None:
    """
    Parse the README.md (v2) to extract per-talk metadata.

    The README has sections like:
        ## Meetup #N - YYYY-MM-DD - City
        - **Talk #NN** - Title by Speaker - [**Slides**](path) - [**Video (XX)**](url)
        - **No permission to share**

    Populates meta[event_dirname] -> list of talk metadata dicts.
    """
    # Map README section headers to directory names
    event_patterns = {
        "meetup #1 - 2022-07-16 - london": "2022-07-16-london",
        "meetup #2 - 2022-09-24 - new york city": "2022-09-24-nyc",
        "meetup #3 - 2023-04-08 - tokyo": "2023-04-08-tokyo",
        "meetup #4 - 2023-07-08 - prague": "2023-07-08-prague",
        "meetup #5 - 2023-10-14 - toronto": "2023-10-14-toronto",
        "meetup #6 - 2024-01-16 - san francisco": "2024-01-16-san-francisco",
        "meetup #7 - 2024-04-27 - frankfurt": "2024-04-27-frankfurt",
        "meetup #8 - 2024-07-20 - tokyo": "2024-07-20-tokyo",
        "meetup #9 - 2024-11-11 - bangkok": "2024-11-11-bangkok",
        "meetup #10 - 2025-03-29 - decentralized ai day (seattle)": "2025-03-29-seattle",
        "meetup #11 - 2025-05-17 - decentralized ai day (tokyo)": "2025-05-17-tokyo",
        "meetup #12 - 2025-09-20 - decentralized ai day (vienna)": "2025-09-20-vienna",
        "meetup #13 - 2026-01-27 - decentralized ai day (san francisco)": "2026-01-27-san-francisco",
        "meetup #14 - 2026-03-21 - decentralized ai day (vienna) 2026": "2026-03-21-vienna",
        "meetup #15 - 2026-05-30 - decentralized ai day (tokyo) 2026": "2026-05-30-tokyo",
    }

    lines = content.split("\n")
    current_dirname = None
    event_start_line = -1

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Check for event section header
        for pattern, dirname in event_patterns.items():
            if pattern in line_lower:
                current_dirname = dirname
                event_start_line = i
                if current_dirname not in meta:
                    meta[current_dirname] = []
                break

        if current_dirname is None:
            continue

        # Skip lines that are clearly not content (blank, Eventbrite links, etc.)
        if not line_stripped:
            continue

        # Only process list items and their children
        if not line_stripped.startswith("-") and not line_stripped.startswith("*"):
            continue

        # Pre-detect marker flags for later use
        _has_no_perm = "no permission to share" in line_stripped.lower()
        _has_contact = "contact speaker" in line_stripped.lower()
        _has_couldnt_attend = ("couldn't attend" in line_stripped.lower() or
                               "jos couldn't join" in line_stripped.lower())

        # Check for Welcoming Remarks
        welcome_match = re.match(
            r"\s*[-*]\s+\*\*(Welcoming Remarks|Quick Update(?: on Numerai Meetups)?)\*\*",
            line, re.IGNORECASE
        )
        if welcome_match:
            talk_title = welcome_match.group(1)
            speaker = ""
            video_list = []

            # Try to parse speaker from "by ..."
            rest = line[welcome_match.end():]
            by_match = re.search(r"\s+by\s+(.+?)(?:\s+-|\s*$)", rest)
            if by_match:
                speaker = by_match.group(1).strip()

            # Check for video link
            _extract_video_urls(rest, video_list)

            # Check for slides link
            has_slides = "[**slides**]" in rest.lower()

            meta[current_dirname].append({
                "talk_num": "00",
                "title": talk_title,
                "speaker": speaker,
                "videos": video_list,
                "has_slides": has_slides,
                "no_permission": _has_no_perm,
                "not_shared": _has_couldnt_attend or _has_contact,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # Check for Fireside Chat
        fireside_match = re.match(
            r"\s*[-*]\s+\*\*(The Numerai Community Fireside Chat)\*\*",
            line, re.IGNORECASE
        )
        if fireside_match:
            rest = line[fireside_match.end():]
            video_list = []
            _extract_video_urls(rest, video_list)

            meta[current_dirname].append({
                "talk_num": "99",
                "title": "The Numerai Community Fireside Chat",
                "speaker": "Council of Elders",
                "videos": video_list,
                "has_slides": False,
                "no_permission": _has_no_perm,
                "not_shared": _has_couldnt_attend or _has_contact,
                "is_fireside": True,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # Check for Closing Remarks
        closing_match = re.match(
            r"\s*[-*]\s+\*\*(Closing Remarks)\*\*",
            line, re.IGNORECASE
        )
        if closing_match:
            rest = line[closing_match.end():]
            video_list = []
            _extract_video_urls(rest, video_list)

            meta[current_dirname].append({
                "talk_num": "99",
                "title": "Closing Remarks",
                "speaker": "Council of Elders",
                "videos": video_list,
                "has_slides": False,
                "no_permission": _has_no_perm,
                "not_shared": _has_couldnt_attend or _has_contact,
                "is_fireside": False,
                "is_closing": True,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # Check for Bonus Talk
        bonus_match = re.match(
            r"\s*[-*]\s+\*\*Bonus Talk\b\s*(.*?)\*\*",
            line, re.IGNORECASE
        )
        if bonus_match:
            rest = line[bonus_match.end():]
            bonus_title_raw = bonus_match.group(1).strip()
            speaker = ""
            video_list = []
            has_slides = "[**slides**]" in rest.lower()

            by_match = re.search(r"\s+by\s+(.+?)(?:\s+-|\s*$)", rest)
            if by_match:
                speaker = by_match.group(1).strip()
                # Remove everything up to/by from rest for video/slide detection
                rest_for_assets = rest[by_match.end():]
            else:
                rest_for_assets = rest

            _extract_video_urls(rest_for_assets, video_list)

            # Build title
            if bonus_title_raw:
                talk_num_for_bonus = "99"
                meta[current_dirname].append({
                    "talk_num": talk_num_for_bonus,
                    "title": f"Bonus Talk: {bonus_title_raw}",
                    "speaker": speaker,
                    "videos": video_list,
                    "has_slides": has_slides,
                    "no_permission": _has_no_perm,
                    "not_shared": _has_couldnt_attend or _has_contact,
                    "is_fireside": False,
                    "is_closing": False,
                    "is_bonus": True,
                    "language": "",
                    "snippet": "",
                })
            continue

        # Check for Community Fireside Chart (Prague #4 variant)
        chart_match = re.match(
            r"\s*[-*]\s+\*\*Community Fireside Chart\*\*",
            line, re.IGNORECASE
        )
        if chart_match:
            rest = line[chart_match.end():]
            video_list = []
            _extract_video_urls(rest, video_list)

            meta[current_dirname].append({
                "talk_num": "99",
                "title": "Community Fireside Chat",
                "speaker": "Council of Elders",
                "videos": video_list,
                "has_slides": False,
                "no_permission": _has_no_perm,
                "not_shared": _has_couldnt_attend or _has_contact,
                "is_fireside": True,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # Check for Talk #N(N) pattern
        talk_match = re.match(
            r"\s*[-*]\s+\*\*Talk #([\d.]+[a-z]?)\*\*\s+-\s+(.+?)(?:\s+-\s+\[?\*\*Slides)",
            line, re.IGNORECASE
        )
        if talk_match:
            tn = talk_match.group(1)
            title_speaker = talk_match.group(2)

            # Parse "Title by Speaker"
            by_match = re.search(r"\s+by\s+(.+)$", title_speaker, re.IGNORECASE)
            if by_match:
                talk_title = title_speaker[:by_match.start()].strip()
                rm_speaker = by_match.group(1).strip()
            else:
                talk_title = title_speaker.strip()
                rm_speaker = ""

            # Extract slides/video from the rest of the line
            rest = line[talk_match.end() - 4:]  # rewind to capture full line after "Slides"

            # Parse all asset links from the line
            slides_links = re.findall(
                r"\[(?:\*\*)?Slides(?:\s*\(([^)]*)\))?(?:\*\*)?\]\(([^)]+)\)",
                line, re.IGNORECASE
            )
            video_links = re.findall(
                r"\[(?:\*\*)?Video(?:\s*\(([^)]*)\))?(?:\*\*)?\]\(([^)]+)\)",
                line, re.IGNORECASE
            )

            video_list = []
            for lang, url in video_links:
                video_list.append({"lang": lang.strip() if lang else "", "url": url})

            # Detect "No permission to share" inline on this talk line
            _has_inline_no_perm = "no permission to share" in line_stripped.lower()

            meta[current_dirname].append({
                "talk_num": tn,
                "title": talk_title,
                "speaker": rm_speaker,
                "videos": video_list,
                "has_slides": len(slides_links) > 0,
                "no_permission": _has_inline_no_perm,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # Check for Talk #N(N) without slides (video-only or no-permission)
        talk_match_noslides = re.match(
            r"\s*[-*]\s+\*\*Talk #([\d.]+[a-z]?)\*\*\s+-\s+(.+)",
            line, re.IGNORECASE
        )
        if talk_match_noslides and not talk_match:
            tn = talk_match_noslides.group(1)
            title_speaker = talk_match_noslides.group(2).strip()

            # Strip trailing markdown asset links from title (e.g. " - [**Video**](url)")
            title_speaker_clean = re.sub(
                r"\s+-\s+\[(?:\*\*)?(?:Slides|Video)(?:[^]]*)\](?:\([^)]*\))?\s*$",
                "", title_speaker
            ).strip()

            by_match = re.search(r"\s+by\s+(.+?)(?:\s+-\s+|\s*$)", title_speaker_clean, re.IGNORECASE)
            if by_match:
                talk_title = title_speaker_clean[:by_match.start()].strip()
                rm_speaker = by_match.group(1).strip()
            else:
                talk_title = title_speaker_clean
                rm_speaker = ""

            # Check for video links
            video_links = re.findall(
                r"\[(?:\*\*)?Video(?:\s*\(([^)]*)\))?(?:\*\*)?\]\(([^)]+)\)",
                line, re.IGNORECASE
            )

            video_list = []
            for lang, url in video_links:
                video_list.append({"lang": lang.strip() if lang else "", "url": url})

            # Detect "No permission to share" inline on this talk line
            _has_inline_no_perm = "no permission to share" in line_stripped.lower()
            _has_inline_contact = "contact speaker" in line_stripped.lower()

            meta[current_dirname].append({
                "talk_num": tn,
                "title": talk_title,
                "speaker": rm_speaker,
                "videos": video_list,
                "has_slides": False,
                "no_permission": _has_inline_no_perm,
                "not_shared": _has_inline_contact,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": "",
            })
            continue

        # YIEDL events (Vienna #14 and beyond) - Session blocks
        # These have **Description:** lines under the workshop, then **[Session N]** blocks
        # The workshop sections are nested under bullet points, so we need to handle
        # session parsing separately when we detect the YIEDL context

        # Check for Welcoming Remarks at [indent level]
        # (already handled above)

        # If we reached here, this line didn't match any talk pattern.
        # Check if it's a standalone marker line (e.g. just "No permission to share")
        # and apply to the last talk entry.
        if (_has_no_perm or _has_contact or _has_couldnt_attend) and meta.get(current_dirname):
            if _has_no_perm:
                meta[current_dirname][-1]["no_permission"] = True
            else:
                meta[current_dirname][-1]["not_shared"] = True
        # If it's not a marker line either, log a warning about unparseable line
        elif "talk #" in line_stripped.lower()[:100]:
            print(f"Warning: Could not parse talk line: {line_stripped[:120]}", file=sys.stderr)

    # Post-process: handle YIEDL event sections
    # For Vienna #14: parse YIEDL sections in context (they are inline in the README)
    _parse_yiedl_vienna_sections(content, meta)
    # For San Francisco #13: parse YIEDL sections which have a different structure
    _parse_yiedl_sf_sessions(content, meta)

    # Post-process: fix talk numbers for special entries that need unique numbers
    _assign_talk_numbers(meta)


def _extract_video_urls(line: str, video_list: list) -> None:
    """Extract video URLs from a line and append to video_list."""
    video_links = re.findall(
        r"\[(?:\*\*)?Video(?:\s*\(([^)]*)\))?(?:\*\*)?\]\(([^)]+)\)",
        line, re.IGNORECASE
    )
    for lang, url in video_links:
        video_list.append({"lang": lang.strip() if lang else "", "url": url})


def _parse_yiedl_vienna_sections(content: str, meta: dict[str, list[dict]]) -> None:
    """
    Parse YIEDL workshop sections from events #13 (San Francisco) and #14 (Vienna).
    These have the format:
        - **[Session N] Title — Duration**
        - **[Intro] Title — Duration**
    Each session is indexed as a separate talk.
    """
    # YIEDL sections are found under bullet points like:
    #  - **[Session 1] The Scientist Track: Proving Your Edge — 45 min**
    # We need to find them in context of each event section.

    lines = content.split("\n")

    # Map event headers to their dirnames — only Vienna #14, which has inline YIEDL content
    # SF #13 has YIEDL content under a separate structure handled by _parse_yiedl_sf_sessions
    header_to_dirname = {
        "meetup #14 - 2026-03-21 - decentralized ai day (vienna) 2026": "2026-03-21-vienna",
    }

    # Find YIEDL sections by looking for the workshop bullet points
    current_dirname = None
    yiedl_context = False

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()

        # Detect event header
        for header, dirname in header_to_dirname.items():
            if header in line_lower:
                current_dirname = dirname
                yiedl_context = False
                break

        if current_dirname is None:
            continue

        # Detect YIEDL workshop context - only activate for actual YIEDL sections
        if "yiedl" in line_lower and ("workshop" in line_lower or "session" in line_lower):
            yiedl_context = True
            continue

        # Detect Crunch Workshop to deactivate YIEDL context
        if ("crunch" in line_lower and "workshop" in line_lower) or \
           ("allora" in line_lower and "workshop" in line_lower):
            yiedl_context = False
            continue

        if not yiedl_context:
            # Also check for "**Description:**" which may indicate the start
            if "**description:**" in line:
                continue  # Just continue tracking context
            else:
                # Check if we're near YIEDL content
                pass

        # Parse session blocks when in YIEDL context
        # Match:  - **[Intro] Title — Duration**
        intro_match = re.match(
            r"\s*[-*]\s+\*\*\[Intro\]\s+(.+?)\s*[—–-]+\s*\d+\s*min\b",
            line
        )
        if intro_match and yiedl_context:
            title = intro_match.group(1).strip()
            meta[current_dirname].append({
                "talk_num": "yiedl-intro",
                "title": title,
                "speaker": "YIEDL.ai",
                "videos": [],
                "has_slides": False,
                "no_permission": False,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": f"{title} — workshop session from YIEDL at {event_name_for_dirname(current_dirname, meta)}",
            })
            continue

        # Match:  - **[Session N] Title — Duration**
        session_match = re.match(
            r"\s*[-*]\s+\*\*\[Session\s+(\d+)\]\s+(.+?)\s*[—–-]+\s*\d+\s*min\b",
            line
        )
        if session_match and yiedl_context:
            sn = session_match.group(1)
            title = session_match.group(2).strip()
            meta[current_dirname].append({
                "talk_num": f"yiedl-s{sn}",
                "title": title,
                "speaker": "YIEDL.ai",
                "videos": [],
                "has_slides": False,
                "no_permission": False,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": f"{title} — workshop session {sn} from YIEDL",
            })
            continue

        # Another pattern: without duration in the title
        intro_match2 = re.match(
            r"\s*[-*]\s+\*\*\[Intro\]\s+(.+?)\s*\*\*",
            line
        )
        if intro_match2 and yiedl_context:
            title = intro_match2.group(1).strip()
            meta[current_dirname].append({
                "talk_num": "yiedl-intro",
                "title": title,
                "speaker": "YIEDL.ai",
                "videos": [],
                "has_slides": False,
                "no_permission": False,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": f"{title} — workshop session from YIEDL",
            })
            continue

        # Check for other workshop sections
        # Crunch Workshop sessions
        crunch_intro_match = re.match(
            r"\s*[-*]\s+\*\*\[Intro\]\s+-.+?\*\*",
            line
        )
        if crunch_intro_match and yiedl_context:
            pass  # Handled above

    # End of _parse_yiedl_vienna_sections


def event_name_for_dirname(dirname: str, meta: dict) -> str:
    """Get event name for a dirname from the meta context."""
    if dirname in EVENT_INFO:
        return EVENT_INFO[dirname]["event"]
    return dirname


def _parse_yiedl_sf_sessions(content: str, meta: dict[str, list[dict]]) -> None:
    """Parse YIEDL sessions from the San Francisco (#13) event."""
    # SF event has:
    # - **YIEDL Workshop**
    #   - Description: ...
    #   - **[Intro] The Vision: Bridging Research and Capital — 30 min**
    #   - **[Session 1] The Scientist Track: Proving Your Edge — 45 min**
    #   - etc.
    # The Crunch Workshop section comes AFTER YIEDL and must NOT be parsed here.

    lines = content.split("\n")
    in_sf_yiedl = False
    dirname = "2026-01-27-san-francisco"

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        if "meetup #13" in line_lower or "decentralized ai day (san francisco)" in line_lower:
            in_sf_yiedl = False
            continue

        if "yiedl workshop" in line_lower:
            in_sf_yiedl = True
            continue

        # Stop at Crunch Workshop — it's after YIEDL and has its own [Intro]/[Session] blocks
        if in_sf_yiedl and "crunch workshop" in line_lower:
            in_sf_yiedl = False
            continue

        if not in_sf_yiedl:
            continue

        # Stop at next event header
        if line_stripped.startswith("## ") and "meetup" in line_lower:
            in_sf_yiedl = False
            continue

        # Parse session patterns (YIEDL sessions have NO dash after [Intro])
        # Format: - **[Intro] The Vision: Bridging Research and Capital — 30 min**
        intro_match = re.match(
            r"\s*[-*]\s+\*\*\[Intro\]\s+([A-Za-z][^—–-]+?)\s*[—–-]+\s*\d+\s*min\b",
            line
        )
        if intro_match:
            title = intro_match.group(1).strip()
            meta[dirname].append({
                "talk_num": "yiedl-intro",
                "title": title,
                "speaker": "YIEDL.ai",
                "videos": [],
                "has_slides": False,
                "no_permission": False,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": f"{title} — workshop session from YIEDL at {event_name_for_dirname(dirname, meta)}",
            })
            continue

        session_match = re.match(
            r"\s*[-*]\s+\*\*\[Session\s+(\d+)\]\s+(.+?)\s*[—–-]+\s*\d+\s*min\b",
            line
        )
        if session_match:
            sn = session_match.group(1)
            title = session_match.group(2).strip()
            meta[dirname].append({
                "talk_num": f"yiedl-s{sn}",
                "title": title,
                "speaker": "YIEDL.ai",
                "videos": [],
                "has_slides": False,
                "no_permission": False,
                "not_shared": False,
                "is_fireside": False,
                "is_closing": False,
                "is_bonus": False,
                "language": "",
                "snippet": f"{title} — workshop session {sn} from YIEDL",
            })
            continue

        # Stop when we hit another workshop section clearly not YIEDL
        if line_stripped.startswith("- **") and "workshop" in line_lower and "yiedl" not in line_lower:
            in_sf_yiedl = False


def _assign_talk_numbers(meta: dict[str, list[dict]]) -> None:
    """
    Post-process to assign unique talk numbers for special entries
    (fireside chats, closing remarks, bonus talks) and normalize
    all talk numbers to zero-padded 2-digit format.
    """
    for dirname, talks in meta.items():
        # Find the highest real talk number
        max_num = 0
        for t in talks:
            tn = t["talk_num"]
            if re.match(r"^\d+$", tn):
                max_num = max(max_num, int(tn))

        next_num = max_num + 1

        # Renumber special entries (fireside, closing, bonus) with numbers after max
        for t in talks:
            if t["talk_num"] == "99":
                t["talk_num"] = str(next_num)
                next_num += 1

        # YIEDL entries: assign numbers starting well above max talk numbers
        # to avoid collision with regular numbered talks
        yiedl_nums = [t for t in talks if t["talk_num"].startswith("yiedl-")]
        # Calculate a generous offset: max_num + 20 to stay well clear
        yiedl_offset = max_num + 20
        for t in yiedl_nums:
            t["talk_num"] = str(yiedl_offset)
            yiedl_offset += 1

        # Normalize all numeric talk numbers to zero-padded 2-digit format
        # so they merge correctly with PDF talk numbers (which use "01", "02", etc.)
        for t in talks:
            tn = t["talk_num"]
            digits = re.sub(r"[a-z]", "", tn)
            letter = tn[len(digits):] if tn else tn
            if digits.isdigit():
                t["talk_num"] = f"{int(digits):02d}{letter}"


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <meetups_root> <output_path>", file=sys.stderr)
        sys.exit(1)

    meetups_root = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isdir(meetups_root):
        print(f"Error: {meetups_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    entries = build_index(meetups_root)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output = OrderedDict()
    output["version"] = 2
    output["generatedAt"] = now
    output["entryCount"] = len(entries)
    output["entries"] = entries

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Built v2 cross-source index: {len(entries)} entries -> {output_path}")


if __name__ == "__main__":
    main()
