from ftplib import FTP
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

FTP_SERVER = 'ftp.dlptest.com'
USERNAME = 'dlpuser'
PASSWORD = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

def connect_ftp():
    ftp = FTP(FTP_SERVER)
    ftp.login(user=USERNAME, passwd=PASSWORD)
    ftp.set_pasv(True)
    logging.info(f"Connected to {FTP_SERVER} in passive mode")
    return ftp

def upload_file(ftp, local_file, remote_file):
    if not os.path.exists(local_file):
        raise FileNotFoundError(f"{local_file} not found.")

    with open(local_file, 'rb') as f:
        ftp.storbinary(f'STOR {remote_file}', f)
    logging.info(f"Uploaded {local_file} as {remote_file}")

    if remote_file in ftp.nlst():
        logging.info("Upload confirmed!")
    else:
        logging.error("Upload failed!")

def download_file(ftp, remote_file, local_file):
    with open(local_file, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_file}', f.write)
    logging.info(f"Downloaded {remote_file} as {local_file}")

    with open(local_file, 'r') as f:
        content = f.read()
        print("\n[Downloaded File Content]")
        print(content)

def list_directory(ftp):
    logging.info("Directory listing on server:")
    ftp.retrlines('LIST')

def main():
    ftp = connect_ftp()

    local_upload_file = "test_upload.txt"
    remote_file_name = "test_upload.txt"
    local_download_file = "test_download.txt"

    # Create a sample file to upload
    with open(local_upload_file, 'w') as f:
        f.write("Hello FTP Server!\nThis is a test file.")

    try:
        print("\n[Before Upload] Directory Contents:")
        list_directory(ftp)

        upload_file(ftp, local_upload_file, remote_file_name)

        print("\n[After Upload] Directory Contents:")
        list_directory(ftp)

        download_file(ftp, remote_file_name, local_download_file)

    except Exception as e:
        logging.error(f"FTP operation failed: {e}")

    finally:
        ftp.quit()
        logging.info("FTP connection closed.")
        if os.path.exists(local_upload_file):
            os.remove(local_upload_file)
        if os.path.exists(local_download_file):
            os.remove(local_download_file)

if __name__ == "__main__":
    main()
