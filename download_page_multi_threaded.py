import re
import os
import json
import time
import math
from threading import Thread
from pypdf import PdfWriter
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options to automatically download files to the default location and handle print-to-PDF
chrome_options = webdriver.ChromeOptions()
NUM_PAGES = 428
DOWNLOAD_FOLDER = Path(r"C:\Users\Someone\Downloads")
URL = "https://kotar-cet-ac-il.ezlibrary.technion.ac.il/KotarApp/Viewer.aspx?nBookID=113333418"
BOOK_ID = re.search(r"nBookID=(\d+)", URL).group(1)
EXPECTED_FILES_NUM = math.ceil(NUM_PAGES / 10)
OUT_FILE_PATH = DOWNLOAD_FOLDER.joinpath("new_result_other_file.pdf")
DONE_PAGES = []

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


# Function to save a single batch of 10 pages as a PDF
def save_10_pages_file(driver, url: str):
    driver.get(url)
    try:
        # Wait for the page to fully load and become interactable
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "cr-button.action-button"))
        )
        time.sleep(5)  # Ensure the page has fully rendered and is stable
        driver.execute_script('window.print();')
        WebDriverWait(driver, 10).until(EC.url_changes(url))
        time.sleep(3)  # Wait for the PDF to be saved

    except Exception as e:
        pass


def merge_pdfs(file_paths):
    writer = PdfWriter()
    for pdf in file_paths:
        writer.append(pdf)
    final_path = DOWNLOAD_FOLDER.joinpath(OUT_FILE_PATH)
    with open(final_path, "wb") as f_out:
        writer.write(f_out)
    for pdf in file_paths:
        if os.path.exists(pdf):
            os.remove(pdf)
    print(f"Merged PDFs successfully into {OUT_FILE_PATH}")


def save_10_pages(driver, start_page: int, end_page: int, file_paths: list):
    # print("Saving pages", start_page, "to", end_page)
    global DONE_PAGES
    url = f"https://kotar-cet-ac-il.ezlibrary.technion.ac.il/KotarApp/Viewer/Popups/PrintPages.aspx?nBookID={BOOK_ID}&nPageStart={start_page}&nPageEnd={end_page}"
    file_name = f"kotar-cet-ac-il.ezlibrary.technion.ac.il_KotarApp_Viewer_Popups_PrintPages.aspx_nBookID={BOOK_ID}&nPageStart={start_page}&nPageEnd={end_page}.pdf"
    file_path = DOWNLOAD_FOLDER.joinpath(file_name)
    file_paths.append(file_path)
    save_10_pages_file(driver=driver, url=url)
    DONE_PAGES.append({
        "start": start_page,
        "end": end_page
    })
    if os.path.exists(file_path):
        print(f"Saved pages {start_page} to {end_page}")


def worker(start, end, file_paths):
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
    driver.refresh()

    try:
        for i in range(start, end, 10):
            save_10_pages(driver=driver, start_page=i + 1, end_page=min(i + 10, end), file_paths=file_paths)
    finally:
        driver.quit()


def find_dict_with_start_value(lst, value):
    for d in lst:
        if d.get("start") == value:
            return d
    return None


def check_done_pages():
    global DONE_PAGES
    start = 1
    for _ in range(len(DONE_PAGES)):
        d = find_dict_with_start_value(DONE_PAGES, start)
        if d:
            start = d.get("end") + 1
        else:
            print(f"page {start} not found")
            return
    if start != NUM_PAGES + 1:
        print(f"got to page {start - 1} instead of {NUM_PAGES}")


def get_pages():
    file_paths = []
    threads = []
    num_threads = 4  # Number of threads to use
    pages_per_thread = NUM_PAGES // num_threads
    start_page = 0
    end_page = pages_per_thread

    for i in range(num_threads):
        thread = Thread(target=worker, args=(start_page, end_page, file_paths))
        threads.append(thread)
        thread.start()
        start_page = end_page
        if i == num_threads - 2:
            end_page = NUM_PAGES
        else:
            end_page = min(start_page + pages_per_thread, NUM_PAGES)

    for thread in threads:
        thread.join()

    file_paths.sort(key=lambda path: int(re.search(r'nPageStart=(\d+)', str(path)).group(1)))
    merge_pdfs(file_paths)
    check_done_pages()


if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    get_pages()  # Run the main function

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Script completed in {elapsed_time:.2f} seconds.")
