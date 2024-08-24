import re
import os
import json
import time

from pypdf import PdfWriter
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options to automatically download files to the default location and handle print-to-PDF
chrome_options = webdriver.ChromeOptions()
NUM_PAGES = 238
DOWNLOAD_FOLDER = Path(r"C:\Users\Someone\Downloads")
URL = "https://kotar-cet-ac-il.ezlibrary.technion.ac.il/KotarApp/Viewer.aspx?nBookID=109097074"
BOOK_ID = re.search(r"nBookID=(\d+)", URL).group(1)
OUT_FILE_PATH = DOWNLOAD_FOLDER.joinpath("new_result.pdf")

# Preferences for downloading files and print settings
prefs = {
    "download.prompt_for_download": False,  # Disable the "Save As" prompt
    "download.directory_upgrade": True,  # Use the default download directory
    "safebrowsing.enabled": True  # Enable safe browsing
}

# Configure Chrome to automatically save to PDF
print_settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
prefs["printing.print_preview_sticky_settings.appState"] = json.dumps(print_settings)

chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--kiosk-printing')  # Bypass print dialog


# Set up the WebDriver with the configured options
def save_10_pages_file(driver, url: str):
    # Now open the URL that requires authentication
    driver.get(url)

    try:
        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "cr-button.action-button"))
        )

        # Trigger the print command to save as PDF
        time.sleep(2)
        driver.execute_script('window.print();')
        # Optionally, wait for some time to ensure PDF is saved (depends on page complexity)
        WebDriverWait(driver, 10).until(EC.url_changes(url))
    except Exception as e:
        pass


def merge_pdfs(pdf_file_names):
    writer = PdfWriter()
    for pdf in pdf_file_names:
        writer.append(pdf)

    with open(OUT_FILE_PATH, "wb") as f_out:
        writer.write(f_out)

    for pdf in pdf_file_names:
        if os.path.exists(pdf):
            os.remove(pdf)
    print(f"Merged PDFs successfully")


def save_10_pages(driver, start_page: int, end_page: int, file_names: list):
    print("Saving pages", start_page, "to", end_page)
    url = f"https://kotar-cet-ac-il.ezlibrary.technion.ac.il/KotarApp/Viewer/Popups/PrintPages.aspx?nBookID={BOOK_ID}&nPageStart={start_page}&nPageEnd={end_page}"
    file_name = f"kotar-cet-ac-il.ezlibrary.technion.ac.il_KotarApp_Viewer_Popups_PrintPages.aspx_nBookID={BOOK_ID}&nPageStart={start_page}&nPageEnd={end_page}.pdf"
    file_path = DOWNLOAD_FOLDER.joinpath(file_name)
    file_names.append(file_path)
    save_10_pages_file(driver=driver, url=url)


def get_pages():
    file_names = []
    driver = webdriver.Chrome(options=chrome_options)
    # Load cookies before opening the URL
    driver.get("https://kotar-cet-ac-il.ezlibrary.technion.ac.il")
    driver.execute_cdp_cmd('Network.enable', {})
    for cookie in json.loads(Path('cookies.json').read_text()):
        if 'expiry' in cookie:
            cookie['expires'] = cookie['expiry']
            del cookie['expiry']
        driver.execute_cdp_cmd('Network.setCookie', cookie)
    driver.execute_cdp_cmd('Network.disable', {})

    # Refresh to ensure cookies take effect
    driver.refresh()

    try:
        for i in range(0, NUM_PAGES - (NUM_PAGES % 10), 10):
            save_10_pages(driver=driver, start_page=i + 1, end_page=i + 10, file_names=file_names)

        # Handle the last batch of pages
        if NUM_PAGES % 10 != 0:
            i = NUM_PAGES - (NUM_PAGES % 10)
            save_10_pages(driver=driver, start_page=i + 1, end_page=i + (NUM_PAGES % 10), file_names=file_names)
    finally:
        driver.quit()
        file_names.sort(key=lambda path: int(re.search(r'nPageStart=(\d+)', str(path)).group(1)))
        merge_pdfs(file_names)


if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    get_pages()  # Run the main function

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Script completed in {elapsed_time:.2f} seconds.")
