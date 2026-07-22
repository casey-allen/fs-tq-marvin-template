#!/usr/bin/env python3
"""Thin Google Sheets CLI for the Master Lead Tracker — used by cloud routines
where the local google-sheets MCP is unavailable.

Auth: a Google service-account key, from one of
  GSHEETS_SA_JSON  — the key JSON itself (preferred for cloud env secrets)
  GSHEETS_SA_PATH  — path to the key file (local default: ~/.config/marvin/gsheets-sa.json)

Deps: pip install google-auth requests

Commands (all against config.yaml's leads_tracker_sheet_id unless --sheet-id):
  get "<A1 range>"                     print values as JSON
  update "<A1 range>" '<json rows>'    write values (USER_ENTERED)
  find-lead <L-NNN>                    print the 1-based row number of a Lead ID
  next-row                             first empty row in column A (data starts row 3)
  max-id                               highest L-NNN currently assigned

The caller (the routine prompt) owns all schema knowledge — which columns to
write, formula columns to avoid, N/A conventions. This script is deliberately
dumb: auth + ranges only.
"""

import json
import os
import signal
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SHEET_ID = "1mSDdIeERKPoBeaOa_T7lHi5MA4aSOyndz7-Bfd_VfZg"
TAB = "Lead Tracker"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
API = "https://sheets.googleapis.com/v4/spreadsheets"
DRIVE_API = "https://www.googleapis.com/drive/v3/files"
DRIVE_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
DOC_MIME = "application/vnd.google-apps.document"


def _creds():
    raw = os.environ.get("GSHEETS_SA_JSON")
    if raw:
        info = json.loads(raw)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        path = os.environ.get("GSHEETS_SA_PATH", str(Path.home() / ".config/marvin/gsheets-sa.json"))
        creds = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
    creds.refresh(Request())
    return creds


def _headers():
    return {"Authorization": f"Bearer {_creds().token}"}


def get_values(sheet_id, rng):
    r = requests.get(f"{API}/{sheet_id}/values/{requests.utils.quote(rng)}", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json().get("values", [])


def update_values(sheet_id, rng, values):
    r = requests.put(
        f"{API}/{sheet_id}/values/{requests.utils.quote(rng)}",
        headers=_headers(),
        params={"valueInputOption": "USER_ENTERED"},
        json={"values": values},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def doc_create(folder_id, title, markdown):
    """Create a Google Doc in folder_id from markdown (Drive converts). Prints file id + link.
    Requires the folder to be shared (Editor) with the service account."""
    meta = json.dumps({"name": title, "mimeType": DOC_MIME, "parents": [folder_id]})
    body = (
        b"--BOUNDARY\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
        + meta.encode()
        + b"\r\n--BOUNDARY\r\nContent-Type: text/markdown\r\n\r\n"
        + markdown.encode()
        + b"\r\n--BOUNDARY--"
    )
    r = requests.post(
        f"{DRIVE_UPLOAD}?uploadType=multipart&fields=id,webViewLink&supportsAllDrives=true",
        headers={**_headers(), "Content-Type": "multipart/related; boundary=BOUNDARY"},
        data=body,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def doc_replace(file_id, markdown):
    """Replace a Google Doc's entire content from markdown."""
    r = requests.patch(
        f"{DRIVE_UPLOAD}/{file_id}?uploadType=media&supportsAllDrives=true",
        headers={**_headers(), "Content-Type": "text/markdown"},
        data=markdown.encode(),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def doc_read(file_id):
    """Export a Google Doc's current content as markdown (for append-then-replace updates)."""
    r = requests.get(
        f"{DRIVE_API}/{file_id}/export?mimeType=text/markdown",
        headers=_headers(),
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def _hang_guard(signum, frame):
    print("TIMEOUT: no response from googleapis.com within 60s — network egress from this sandbox is likely blocked. Report this exact message.", file=sys.stderr)
    sys.exit(3)


def main():
    signal.signal(signal.SIGALRM, _hang_guard)
    signal.alarm(60)
    args = sys.argv[1:]
    sheet_id = SHEET_ID
    if "--sheet-id" in args:
        i = args.index("--sheet-id")
        sheet_id = args[i + 1]
        del args[i : i + 2]
    if not args:
        print(__doc__)
        sys.exit(1)

    cmd, rest = args[0], args[1:]

    if cmd == "get":
        print(json.dumps(get_values(sheet_id, rest[0])))
    elif cmd == "update":
        print(json.dumps(update_values(sheet_id, rest[0], json.loads(rest[1]))))
    elif cmd == "find-lead":
        col_a = get_values(sheet_id, f"{TAB}!A:A")
        for idx, row in enumerate(col_a, start=1):
            if row and row[0].strip() == rest[0].strip():
                print(idx)
                return
        print("NOT FOUND", file=sys.stderr)
        sys.exit(2)
    elif cmd == "next-row":
        col_a = get_values(sheet_id, f"{TAB}!A:A")
        # data starts at row 3; col_a is trimmed to the last non-empty cell
        print(max(len(col_a) + 1, 3))
    elif cmd == "doc-create":
        # doc-create <folderId> <title>   (markdown on stdin)
        print(json.dumps(doc_create(rest[0], rest[1], sys.stdin.read())))
    elif cmd == "doc-replace":
        # doc-replace <fileId>            (markdown on stdin)
        print(json.dumps(doc_replace(rest[0], sys.stdin.read())))
    elif cmd == "doc-read":
        # doc-read <fileId>               (prints doc content as markdown)
        print(doc_read(rest[0]))
    elif cmd == "max-id":
        col_a = get_values(sheet_id, f"{TAB}!A:A")
        ids = [r[0] for r in col_a if r and r[0].startswith("L-")]
        nums = [int(i.split("-")[1]) for i in ids if i.split("-")[1].isdigit()]
        print(f"L-{max(nums):03d}" if nums else "NONE")
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
