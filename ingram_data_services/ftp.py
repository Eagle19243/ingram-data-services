# -*- coding: utf-8 -*-

import os
from ftplib import FTP

from ingram_data_services import logger
from ingram_data_services.utils import save_history


class RemoteFile:
    """Helper for remote files."""

    def __init__(self, abs_path, facts):
        self.path = abs_path
        self.name = os.path.basename(abs_path)
        self.facts = facts

    @property
    def is_dir(self):
        if self.facts["type"] == "dir":
            return True
        return False

    @property
    def is_file(self):
        if self.facts["type"] == "file":
            return True
        return False

    @property
    def dir_name(self):
        return os.path.dirname(self.path)


class IngramFTP(FTP):
    """Extend the default FTP class."""

    def is_downloaded(self, remote_file, local_file):
        """Determine if we need to download the file."""
        # If the file doesn't exist, then download it
        if not os.path.exists(local_file):
            # logger.debug(f'"{local_file}" does not exist')
            return False

        # If the local/remote files sizes do not match, then download it
        local_size = os.path.getsize(local_file)
        remote_size = self.size(remote_file)
        if local_size != remote_size:
            # logger.debug(f'File size mismatch "{local_file}": {local_size} != {remote_size}')
            return False

        # Passed both exists and filesize checks, assume we have it
        # logger.debug(f'"{local_file}" exists')
        return True

    def download_file(self, remote_file, local_file, force=False):
        """Download a file."""
        # Create the target target_dir
        os.makedirs(os.path.dirname(local_file), exist_ok=True)

        # remote_file_size = self.size(remote_file)
        # modified_date = self.voidcmd(f"MDTM {remote_file}")[4:].strip()

        if not self.is_downloaded(remote_file, local_file) or force is True:
            logger.info(f'Downloading "{remote_file}" => "{local_file}" ...')
            with open(local_file, "wb") as fp:
                self.retrbinary(f"RETR {remote_file}", fp.write)
            # save_history(local_file, remote_file_size, modified_date)

    def get_cover_files(self, folder):
        logger.info(f"Get cover zips from folder {folder} ...")
        paths = []
        image_dir = f"/Imageswk/{folder}"
        for name, facts in self.mlsd(image_dir, ["type"]):
            file = RemoteFile(os.path.join(image_dir, name), facts)
            if ".zip" in file.name and file.is_file:
                paths.append(file.path)
        return paths

    def get_onix_files(self):
        logger.info(f"Get ONIX zip files ...")
        paths = []
        onix_dir = "/ONIX"
        dirs = [
            "Active",
            # "Active_Split",
            "Extended",
            # "Extended_Split",
            "NotAvailable",
            # "NotAvailable_Split",
        ]
        for d in dirs:
            current_dir = os.path.join(onix_dir, d)
            for name, facts in self.mlsd(current_dir, ["type"]):
                file = RemoteFile(os.path.join(current_dir, name), facts)
                if ".zip" in file.name and file.is_file:
                    paths.append(file.path)
        return paths

    def get_onix_bklst_files(self):
        logger.info(f"Get ONIX_BKLST zip files ...")
        paths = []
        onix_bklst_dir = "/ONIX_BKLST"
        for name, facts in self.mlsd(onix_bklst_dir, ["type"]):
            file = RemoteFile(os.path.join(onix_bklst_dir, name), facts)
            if ".zip" in file.name and file.is_file:
                paths.append(file.path)
        return paths

    def get_reference_files(self):
        logger.info(f"Get Reference files ...")
        paths = []
        target_dir = "/Reference_Files"
        files = [
            "bsacmjr.txt",  # BISAC Subject Code – Major
            "bscsjcg.txt",  # BISAC Subject Code – Minor
            "lang.txt",  # Content Language Code
            "prodtp.txt",  # Ingram Product Type
        ]
        for f in files:
            for name, facts in self.mlsd(target_dir, ["type"]):
                file = RemoteFile(os.path.join(target_dir, name), facts)
                if ".txt" in file.name and file.is_file and file.name == f:
                    paths.append(file.path)
        return paths
