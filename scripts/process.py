import os
import re
import sys
import json
import time
import zipfile
import requests

from datetime import datetime
from bs4 import BeautifulSoup

datapackage = "datapackage.json"
# data.un.org now serves the new UN Data Commons site. The original UNdata, with this
# table and its download handler, is kept under /legacy/.
url = "https://data.un.org/legacy/Handlers/DownloadHandler.ashx"
original_url = "https://data.un.org/legacy/Data.aspx?d=POP&f=tableCode:240"
zip_files = ["UNdata_Export_both.zip", "UNdata_Export_fm.zip"]
output_dir = "data"
files = ['unsd-citypopulation-year-both.csv','unsd-citypopulation-year-fm.csv']
footnote_files = ['unsd-citypopulation-year-both-footnotes.csv','unsd-citypopulation-year-fm-footnotes.csv']
sexCode = ['sexCode:0', 'sexCode:1,2']
# Parameters for the first request (sexCode: 0)
params = {
    "DataFilter": "tableCode:240;",
    "DataMartId": "POP",
    "Format": "csv",
    "c": "2,3,6,8,10,12,14,16,17,18",
    "s": "_countryEnglishNameOrderBy:asc,refYear:desc,areaCode:asc"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://data.un.org/legacy/Data.aspx?d=POP&f=tableCode:240",
}

def fetch(address, **kwargs):
    """GET with a few retries: the UN site sometimes answers 502 or 503 for a while."""
    attempts = 5
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(address, headers=headers, **kwargs)
            if response.status_code not in (500, 502, 503, 504):
                response.raise_for_status()
                return response
            message = "HTTP {}".format(response.status_code)
        except (requests.ConnectionError, requests.Timeout) as error:
            message = type(error).__name__
        if attempt == attempts:
            sys.exit("Giving up on {} after {} attempts ({}).".format(address, attempts, message))
        wait = 30 * attempt
        print("{} from the UN site, trying again in {} seconds ({}/{})".format(message, wait, attempt, attempts))
        time.sleep(wait)


def run_download(code, zip_file):
    # Send GET request
    params['DataFilter'] = f"tableCode:240;{code}"
    response = fetch(url, params=params, timeout=300)
    if not response.content.startswith(b"PK"):
        sys.exit("Download from {} is not a ZIP file; the UN site may have changed.".format(url))

    with open(zip_file, "wb") as file:
        file.write(response.content)
    print("File downloaded successfully as {}".format(zip_file))

def run_extract_zip(zip_file, output_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        extracted_file = zip_ref.namelist()[0]
        zip_ref.extract(extracted_file, output_dir)
        extracted_path = os.path.join(output_dir, extracted_file)
        
        # Rename the extracted file
        renamed_path = os.path.join(output_dir, output_file)
        os.rename(extracted_path, renamed_path)
        print(f"File extracted and renamed to: {renamed_path}")

def run_split_footnotes(data_file, footnote_file):
    """The UN export ends with a blank line and a second table of footnotes.
    Move that table into its own file so the data file holds data rows only."""
    marker = b'"footnoteSeqID","Footnote"'
    data_path = os.path.join(output_dir, data_file)
    with open(data_path, "rb") as f:
        content = f.read()
    if content.count(marker) != 1:
        sys.exit("Expected one footnote table in {}, found {}.".format(data_file, content.count(marker)))
    position = content.index(marker)
    with open(data_path, "wb") as f:
        f.write(content[:position].rstrip(b"\r\n") + b"\r\n")
    with open(os.path.join(output_dir, footnote_file), "wb") as f:
        f.write(content[position:])
    print(f"Footnotes moved to: {footnote_file}")


def run_date_conversion():
    date_pattern = r"\d{4}/\d{2}/\d{2}"

    response = fetch(original_url, timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", class_="Update")
    if div is None:
        sys.exit("No update dates found on {}; the UN page may have changed.".format(original_url))

    dates = re.findall(date_pattern, div.text)
    if len(dates) < 2:
        sys.exit("Expected a last and a next update date on {}, found {}.".format(original_url, dates))
    formatted_dates = [datetime.strptime(date, "%Y/%m/%d").strftime("%d %b %Y") for date in dates]

    return formatted_dates

def run_update_datapackage(date):
    try:
        with open(datapackage, "r", encoding="utf-8") as file:
            data = json.load(file)

        formatted_date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")
        print(f"Last Updated date from the source: {formatted_date}")

        data['last_updated'] = formatted_date
        with open(datapackage, "w", encoding="utf-8", newline="") as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print("datapackage.json updated successfully!")
    
    except FileNotFoundError:
        print(f"Error: The file '{datapackage}' does not exist.")

if __name__ == '__main__':
    # Download everything first, so a failed download leaves the data files untouched.
    dates = run_date_conversion()
    for code, zip_file in zip(sexCode, zip_files):
        print(f"Downloading file with code: {code}")
        run_download(code, zip_file)
    for zip_file, file, footnote_file in zip(zip_files, files, footnote_files):
        print("Extracting ZIP file...")
        run_extract_zip(zip_file, file)
        print("Moving the footnotes into their own file...")
        run_split_footnotes(file, footnote_file)
        os.remove(zip_file)
        print("Zip File removed.")
    print("Process completed.")
    run_update_datapackage(dates[0])
