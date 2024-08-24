# kotarPdfDownloader
## How To download the pdf:
* Make sure to run `pip install -r requirements.txt` and that the packages installed are visible on the PATH of your current environment.
* Download Extension "EditThisCookie" from ChromeStore
* While you are on the Kotar book's webpage, click on the extension and choose to Export the cookie (it will copy the needed cookies to your clipboard)
* Save the cookies copied by the extension into a file named "cookies.json" and make sure the file and the script are in the same folder.
* Inside the Script itself change the constants : "NUM_PAGES", "DOWNLOAD_FOLDER", "URL", "OUT_FILE_NAME" in config.json if needed.
* the "DOWNLOAD_FOLDER" should be chrome's default download folder as defined in your browser.

Command to run the script (Assuming the script is in the directory you are currently on): 

`python3 .\download_page.py`

Or if you want the multithreaded version (faster but less stable)

`python3 .\download_page_multi_threaded.py`

## How To crop the pdf
* Make sure to run `pip install -r requirements.txt` and that the packages installed are visible on the PATH of your current environment.
* Update "input_pdf", "output_pdf" in the script if needed, and "CROP_MARGIN" in the config.py file if needed.

Command to run the script (Assuming the script is in the directory you are currently on):

`python3 .\crop_pdf.py`