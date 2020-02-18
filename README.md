# Ingram Data Service

Command line tool to connect to Ingram Data Services FTP and download
cover images, Onix and Reference zip files. Once downloaded, extracts
them to a working dir for further processing by `ingram-onix`.


## Data Storage
The amount of data and storage requirements will vary per data license. The
approximate storage per title or bibliographic data = 20KB and for a JPEG 400
pixel image = 35KB.


## Config
Create a `~/finderscope/config/ingram-data-services.cfg` file with the following contents:

    [default]
    host=ftp.ingramcontent.com
    user=USER
    passwd=PASS
    cover_size=J648h
    download_dir=/Volumes/Extreme SSD
    working_dir=/Volumes/Extreme SSD/working

    [test]
    host=ftptest.ingramcontent.com
    user=USER
    passwd=PASS
    cover_size=J400w
    download_dir=/Volumes/Extreme SSD/TEST
    working_dir=/Volumes/Extreme SSD/TEST_WORKING


## Requirements

* Python 3.7+


## Installation

    python setup.py install


## Usage

    usage: ingram-data-services [--config-section CONFIG_SECTION]

    Login and pull data from Ingram's FTP server

    optional arguments:
    --config-section CONFIG_SECTION
                            config section to use
    --log-file LOG_FILE   location to log the history
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    example: ingram-data-services --config-section test


## Resources
- [Ingram Data Services](https://www.ingramcontent.com/retailers/ingram-data-services)
