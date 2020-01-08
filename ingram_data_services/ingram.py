# -*- coding: utf-8 -*-

"""
It is imperative that you process all delta files in sequential order.

You should process delta files first and then deletes.

When processing deletes, you must also process deletes for all of your tables
that are directly related to the item (images, descriptions, etc...these are
files that contain a primary key of EAN). This is required to stay in
compliance with your data license and maintain data integrity.
"""

import argparse
import configparser
import fnmatch
import logging
import multiprocessing
import os
import sys
from zipfile import ZipFile

from . import utils
from .__version__ import __version__
from .ftp import IngramFTP

logger = logging.getLogger(__name__)

host = None
user = None
passwd = None
pool = None


def get_parser():
    """Returns the Argument Parser."""
    parser = argparse.ArgumentParser(
        description="Login and pull data from Ingram's FTP server"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    return parser


def get_config():
    """Read the config file."""
    config_file = os.path.expanduser("~/finderscope/config/ingram-data-services.cfg")
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    raise RuntimeError(f'"{config_file}" does not exist')


def download_file(remote_file, download_dir):
    """Helper to allow multiprocessing."""
    # Create the local file path
    local_file = os.path.join(
        download_dir,
        os.path.dirname(remote_file).lstrip("/"),
        os.path.basename(remote_file),
    )

    # We can't download multiple files from FTP at once, so we need to
    # create an FTP instance and login for each download
    with IngramFTP(host=host, user=user, passwd=passwd) as ftp:
        try:
            ftp.download_file(remote_file, local_file)
        except KeyboardInterrupt:
            pool.terminate()


def download_data_files(download_dir, concurrent_downloads):
    logger.info("Download Ingram data files ...")
    with IngramFTP(host=host, user=user, passwd=passwd) as ftp:
        # logger.info(f"Connected to {host}...")
        # logger.info(f"Welcome message: {ftp.getwelcome()}")

        cover_paths = ftp.get_cover_files(folder="J400w")
        onix_paths = ftp.get_onix_files()
        ref_paths = ftp.get_reference_files()

        # Assemble our tuple of args for the download method
        cover_paths = [(p, download_dir) for p in cover_paths]
        onix_paths = [(p, download_dir) for p in onix_paths]
        ref_paths = [(p, download_dir) for p in ref_paths]

    # Process the downloads
    logger.debug("Concurrent downloads: %s", concurrent_downloads)
    pool = multiprocessing.Pool(processes=concurrent_downloads)
    pool.starmap(download_file, cover_paths)
    pool.starmap(download_file, onix_paths)
    pool.starmap(download_file, ref_paths)
    pool.close()
    pool.join()


def extract_cover_zip(file, target_dir):
    """Extract files one by one so we can organize into folders
    based on last 4 of ISBN for faster access."""
    with ZipFile(file, "r") as zf:
        filenames = zf.namelist()
        for f in filenames:
            subdir, _ = os.path.splitext(f)
            zf.extract(f, os.path.join(target_dir, subdir[-4:]))


def extract_zip(file, target_dir):
    """Extract files from zip"""
    if not os.path.isdir(target_dir):
        with ZipFile(file, "r") as zf:
            zf.extractall(target_dir)


def main():
    global host, user, passwd, pool

    # Ensure proper command line usage
    args = get_parser().parse_args()

    # Read our config file
    config = get_config()

    host = config.get("default", "host")
    user = config.get("default", "user")
    passwd = config.get("default", "passwd")

    download_dir = os.path.expanduser(config.get("default", "download_dir"))
    concurrent_downloads = config.getint("default", "concurrent_downloads")
    working_dir = os.path.expanduser(config.get("default", "working_dir"))

    # Download data files
    download_data_files(download_dir, concurrent_downloads)

    # Unzip data files
    logger.info("Unzip cover zips ...")
    cover_zips = utils.get_files_matching(
        os.path.join(download_dir, "Imageswk"), "*.zip"
    )
    # for z in cover_zips:
    #     extract_cover_zip(z, os.path.join(working_dir, "covers"))

    covers = utils.get_files_matching(os.path.join(working_dir, "covers"), "*.jpg")
    logger.info(f"Number of covers: {len(covers)}")

    # Unzip data files
    logger.info("Unzip ONIX zips ...")
    data_zips = utils.get_files_matching(os.path.join(download_dir, "ONIX"), "*.zip")
    for z in data_zips:
        extract_dir = os.path.dirname(z).replace(download_dir, "").lstrip("/")
        extract_dir = os.path.join(working_dir, extract_dir)
        extract_zip(z, extract_dir)
