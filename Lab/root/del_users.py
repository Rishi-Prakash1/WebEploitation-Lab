#!/usr/bin/env python3
"""del_users.py - runs at container start (stands in for @reboot).
Resets the users table so every boot starts from a clean registration state."""
import sys

import mysql.connector

LOG = "/var/log/del_users.log"


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
        cursor.execute("TRUNCATE TABLE users")
        mydb.close()
        log("users table truncated")
        return 0
    except mysql.connector.Error as exc:
        log("db error: %s" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
