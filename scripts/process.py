import os
import re
import json
import zipfile
import requests

from datetime import datetime
from bs4 import BeautifulSoup

readme_file = "README.md"
datapackage = "datapackage.json"
url = "https://data.un.org/Handlers/DownloadHandler.ashx"
original_url = 'https://data.un.org/Data.aspx?d=POP&f=tableCode:240'
zip_file = "UNdata_Export.zip"
output_dir = "data"
files = ['unsd-citypopulation-year-both.csv','unsd-citypopulation-year-fm.csv']
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
    "Referer": "https://data.un.org/Data.aspx?d=POP&f=tableCode:240",  # Optional, if required
}

def run_download(code):
    # Send GET request
    params['DataFilter'] = f"tableCode:240;{code}"
    response = requests.get(url, params=params, headers=headers)

    # Save the response content to a file
    if response.status_code == 200:
        with open(zip_file, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully as {}".format(zip_file))
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def run_extract_zip(output_file):
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

def run_date_conversion():
    date_pattern = r"\d{4}/\d{2}/\d{2}"

    response = requests.get(original_url)
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", class_="Update")

    dates = re.findall(date_pattern, div.text)
    formatted_dates = [datetime.strptime(date, "%Y/%m/%d").strftime("%d %b %Y") for date in dates]

    return formatted_dates

def run_update_readme(formatted_dates):
    with open(readme_file, "r") as file:
        readme_content = file.read()

    # Regular expression to locate the relevant section for updates
    pattern = r"#### Updates\nLast update in UNdata: .*?\n\nNext update in UNdata: .*?\n"
    replacement = f"#### Updates\nLast update in UNdata: {formatted_dates[0]}\n\nNext update in UNdata: {formatted_dates[1]}\n"
    updated_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    with open(readme_file, "w") as f:
        f.write(updated_content)

    print("README.md updated successfully!")

def run_update_datapackage(date):
    try:
        with open(datapackage, "r") as file:
            data = json.load(file)

        formatted_date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")
        print(f"Last Updated date from the source: {formatted_date}")

        data['last_updated'] = formatted_date
        with open(datapackage, "w") as file:
            json.dump(data, file, indent=2)
        print("datapackage.json updated successfully!")
    
    except FileNotFoundError:
        print(f"Error: The file '{datapackage}' does not exist.")

if __name__ == '__main__':
    for code, file in zip(sexCode, files):
        print(f"Downloading file with code: {code}")
        run_download(code)
        print("Extracting ZIP file...")
        run_extract_zip(file)
        print("Processing CSV file...")
        os.remove(zip_file)
        print("Zip File removed.")
    print("Process completed.")
    date = run_date_conversion()
    run_update_readme(date)
    run_update_datapackage(date[0])
