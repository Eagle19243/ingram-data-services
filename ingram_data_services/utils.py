# -*- coding: utf-8 -*-

import fnmatch
import logging
import os

logger = logging.getLogger(__name__)


def get_files_matching(input_dir, match="*.zip"):
    """Return all files of a type in the input dir no matter how deep."""
    # logger.info('Get all files matching "%s"' % match)
    matches = []
    for root, dirnames, filenames in os.walk(input_dir):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))
    return matches
