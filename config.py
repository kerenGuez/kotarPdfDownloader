from typing import Dict


class Config:
    NUM_PAGES: int = 238
    DOWNLOAD_FOLDER: str = r"C:\Users\Someone\Downloads"
    URL: str = r"https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=109097074"
    OUT_FILE_NAME: str = "m_result.pdf"
    CROP_MARGIN: Dict[str, int] = {
        "left": 50,
        "right": 140,
        "top": 50,
        "bottom": 175
    }


# Create an instance of the configuration
config = Config()
