import fitz  # PyMuPDF
from pathlib import Path


def crop_pdf(input_pdf_path, output_pdf_path, crop_margin):
    # Open the input PDF
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
    input_pdf = Path(r"C:\Users\Someone\Downloads\result2.pdf")
    output_pdf = Path(r"C:\Users\Someone\Downloads\cropped_example.pdf")

    # Set the margins to be cropped (in points, where 1 point = 1/72 inch)
    crop_margins = {
        "left": 50,    # Crop 50 points from the left
        "right": 175,   # Crop 50 points from the right
        "top": 50,     # Crop 50 points from the top
        "bottom": 175   # Crop 50 points from the bottom
    }

    crop_pdf(input_pdf, output_pdf, crop_margins)
