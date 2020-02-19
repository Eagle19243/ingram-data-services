# -*- coding: utf-8 -*-

import fnmatch
import os
from datetime import datetime

from dateutil import parser, tz

log_dir = None


def get_files_matching(input_dir, match="*.zip"):
    """Return all files of a type in the input dir no matter how deep."""
    matches = []
    for root, dirnames, filenames in os.walk(input_dir):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))
    return matches


def get_local_path(remote_file, download_dir=""):
    """Given a remote path, return its local equivalent."""
    return os.path.join(
        download_dir,
        os.path.dirname(remote_file).lstrip("/"),
        os.path.basename(remote_file),
    )


def set_log_dir(path):
    global log_dir
    log_dir = os.path.expanduser(path)


def save_history(target_filename, remote_file_size, modified_date):
    """Save downloaded filename, filesize, modified date to log file"""
    with open(os.path.join(log_dir, "download_history.log"), "a") as fp:
        fp.write(f"{target_filename} {modified_date} {remote_file_size}\n")


def save_run_history(tz_string="US/Eastern"):
    """Get current time in EST and save it to a file."""
    utc = tz.gettz("UTC")
    ts = datetime.now(tz=utc)
    est = tz.gettz(tz_string)
    run_datetime = ts.astimezone(est)
    with open(os.path.join(log_dir, "run_history.log"), "a") as fp:
        fp.write(f"{run_datetime.isoformat()}\n")


def is_downloaded(target_filename, remote_file_size, modified_date):
    """Check if file already downloaded"""
    ret = False

    if not os.path.isfile(os.path.join(log_dir, "download_history.log")):
        return ret

    with open(os.path.join(log_dir, "download_history.log"), "r") as fp:
        lines = fp.readlines()
        for line in lines:
            if (
                target_filename in line
                and str(remote_file_size) in line
                and modified_date in line
            ):
                ret = True

    return ret
