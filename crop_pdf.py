import fitz  # PyMuPDF
from pathlib import Path
from config import config


def crop_pdf(input_pdf_path=None, output_pdf_path=None, crop_margin=None):
    # Open the input PDF
    if not input_pdf_path:
        input_pdf_path = Path(config.DOWNLOAD_FOLDER).joinpath(config.OUT_FILE_NAME)

    if not output_pdf_path:
        output_pdf_path = Path(config.DOWNLOAD_FOLDER).joinpath("cropped_" + config.OUT_FILE_NAME)

    if not crop_margin:
        crop_margin = config.CROP_MARGIN

    pdf_document = fitz.open(input_pdf_path)

    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        rect = page.rect  # The original page rectangle

        # Define the crop rectangle
        crop_rect = fitz.Rect(
            rect.x0 + crop_margin["left"],
            rect.y0 + crop_margin["top"],
            rect.x1 - crop_margin["right"],
            rect.y1 - crop_margin["bottom"]
        )

        # Set the crop box to the new rectangle
        page.set_cropbox(crop_rect)

    # Save the cropped PDF to the output path
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    print(f"Cropped margins: {crop_margin}")
    print(f"Cropped PDF saved as: {output_pdf_path}")


if __name__ == "__main__":
    # Example usage
    # input_pdf = Path(r"C:\Users\Someone\Downloads\new_result_other_file.pdf")
    # output_pdf = Path(r"C:\Users\Someone\Downloads\cropped_try_example.pdf")
    crop_pdf()
