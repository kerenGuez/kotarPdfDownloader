# kotarPdfDownloader
## How To Use:
* Make sure to run `pip install -r requirements.txt` and that the packages installed are visible the PATH of your current environment
* Download Extension "EditThisCookie" from ChromeStore
* While you are on the open kotar book's webpage, click on the extension and choose to Export the cookie (it will copy the needed cookis to your clipboard)
* Save the cookies copied by the extension into a file named "cookies.json" and make sure the file and the script are in the same folder
* Inside the Script itself change the constants : "NUM_PAGES", "DOWNLOAD_FOLDER", "URL", "OUT_FILE_PATH" to fit your specific case
* the "DOWNLOAD_FOLDER" should be chrome's default download folder as defined in your browser

Command to run the script (Assuming the script is in the directory you are currently on): 
`python3 .\download_page.py`
