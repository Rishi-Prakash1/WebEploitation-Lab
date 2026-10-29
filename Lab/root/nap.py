#!/usr/bin/env python3
"""
nap.py - the "admin bot".

Root cron runs this every 2 minutes. It reads every URL that users have
submitted via the web form, fetches each one, and if the page looks like a
tab-nabbing payload (a location.replace / opener.location redirect) it
follows that redirect and posts the admin credentials to it.

This is the vulnerable-by-design component of the lab. The hardening below
is purely defensive: it keeps one malformed row from killing the whole run.
"""
import re
import sys

import requests
import mysql.connector

LOG = "/var/log/nap.log"

CREDS = {
    "username": "daniel",
    "password": "C@ughtm3napping123",
}

# A URL as it appears inside a JS string: stops at a quote, semicolon,
# whitespace, or closing paren. This replaces the original
# re.findall("http(.*);") / re.findall("http(.*)\);") pair, which required
# a trailing ';' to be present and raised IndexError when it was not.
URL_RE = re.compile(r"""https?://[^\s'"`;)]+""")


def log(msg):
    try:
        with open(LOG, "a") as fh:
            fh.write(msg + "\n")
    except OSError:
        pass


def extract_target(html):
    """Return the URL the payload wants to redirect to, or None.

    Anchors on the redirect keyword and takes the first URL after it, so an
    unrelated <a href> elsewhere in the page cannot be mistaken for the
    exfiltration endpoint. The original regexes scanned the whole document
    and would happily match the wrong URL.
    """
    best = None
    earliest = len(html) + 1
    for kw in ("location.replace", "opener.location"):
        pos = html.find(kw)
        if pos != -1 and pos < earliest:
            earliest = pos
            best = kw

    if best is None:
        return None

    m = URL_RE.search(html, earliest + len(best))
    return m.group(0) if m else None


def main():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",          # TCP, not the Unix socket
            user="adrian",
            password="P@sswr0d456",
            database="website",
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT link FROM links")
        rows = cursor.fetchall()
    except mysql.connector.Error as exc:
        log("db error: %s" % exc)
        return 0

    for row in rows:
        # Defensive: a row could be empty or NULL.
        if not row or not row[0]:
            continue
        url = str(row[0]).strip()
        if not url:
            continue

        try:
            resp = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as exc:
            # Broad on purpose. The original caught only ReadTimeout, so a
            # bare "foo.com" (MissingSchema), "http://" (InvalidURL) or an
            # unsupported scheme (InvalidSchema) aborted the entire run and
            # every subsequent URL went unvisited.
            log("fetch failed %r: %s" % (url, type(exc).__name__))
            continue

        target = extract_target(resp.text)
        if target is None:
            log("no payload in %r" % url)
            continue

        try:
            requests.post(target, data=CREDS, timeout=2)
            log("posted creds to %s" % target)
        except requests.exceptions.RequestException as exc:
            log("post failed %s: %s" % (target, type(exc).__name__))

    try:
        if mydb is not None and mydb.is_connected():
            mydb.close()
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
