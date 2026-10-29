#!/usr/bin/env python3
"""del_links.py - root cron, every 5 minutes. Clears the submitted-link queue."""
import sys

import mysql.connector

LOG = "/var/log/del_links.log"


def log(msg):
    try:
        with open(LOG, "a") as fh:
            fh.write(msg + "\n")
    except OSError:
        pass


def main():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",          # TCP, not the Unix socket
            user="adrian",
            password="P@sswr0d456",
            database="website",
        )
        cursor = mydb.cursor()
        cursor.execute("TRUNCATE TABLE links")
        mydb.close()
        log("links table truncated")
        return 0
    except mysql.connector.Error as exc:
        log("db error: %s" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
