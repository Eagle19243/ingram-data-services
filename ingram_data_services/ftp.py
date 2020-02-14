# -*- coding: utf-8 -*-

import os
from ftplib import FTP
from ingram_data_services import logger
from ingram_data_services.utils import save_history, is_downloaded


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

    def download_file(self, remote_file, local_file, force=False):
        """Download a file."""
        # Create the target target_dir
        target_dir = os.path.dirname(local_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # If we don't have the file, download it
        target_filename = os.path.join(target_dir, os.path.basename(remote_file))
        remote_file_size = self.size(remote_file)
        modified_date = self.voidcmd(f"MDTM {remote_file}")[4:].strip()

        if not is_downloaded(target_filename, remote_file_size, modified_date) or force is True:
            logger.info(f'Downloading "{remote_file}" => "{target_filename}" ...')
            with open(target_filename, "wb") as fp:
                self.retrbinary(f"RETR {remote_file}", fp.write)
            logger.info(f'"{target_filename}" download complete')
            save_history(target_filename, remote_file_size, modified_date)

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
        dirs = ["Active", "Extended", "NotAvailable"]
        for d in dirs:
            current_dir = os.path.join(onix_dir, d)
            for name, facts in self.mlsd(current_dir, ["type"]):
                file = RemoteFile(os.path.join(current_dir, name), facts)
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
