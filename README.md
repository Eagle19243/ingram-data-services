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
    host=ftptest.ingramcontent.com
    user=USER
    passwd=PASS
    download_dir=~/finderscope/ftp_data
    working_dir=~/finderscope/working
    concurrent_downloads=4


## Usage

    ingram-data-services


## Resources
- [Ingram Data Services](https://www.ingramcontent.com/retailers/ingram-data-services)
