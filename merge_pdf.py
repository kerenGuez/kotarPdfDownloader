import os
import sys
from pathlib import Path
from pypdf import PdfWriter


def merge_pdfs(pdf_file_names, out_file_path, should_delete=True):
    writer = PdfWriter()
    for pdf in pdf_file_names:
        writer.append(pdf)

    with open(out_file_path, "wb") as f_out:
        writer.write(f_out)

    if should_delete:
        for pdf in pdf_file_names:
            if os.path.exists(pdf):
                os.remove(pdf)
    print(f"Merged PDFs successfully into {out_file_path}")


def merge_pdfs_from_directory(directory_path, out_file_path, should_delete=True):
    pdf_files = sorted(Path(directory_path).glob("*.pdf"), key=lambda p: p.stem)
    merge_pdfs(pdf_files, out_file_path, should_delete)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python merge_pdf.py <directory> <out_file_path(Default: Current_dir)?> <should_delete_pdfs(True/False)?>")
        sys.exit(1)

    should_delete_pdfs = True
    directory = sys.argv[1]
    if not Path(directory).exists():
        print(f"Error: The directory path '{directory}' is not valid.")
        sys.exit(1)

    the_out_path = Path.cwd().joinpath("merged.pdf")  # Default output path
    if len(sys.argv) >= 3 and sys.argv[2].lower() not in ["true", "false"]:
        the_out_path = Path(sys.argv[2])
        if not the_out_path.parent.exists():
            print(f"Error: The out path '{the_out_path}' is not valid.")
            sys.exit(1)

    if len(sys.argv) == 4 or (len(sys.argv) == 3 and sys.argv[2].lower() in ["true", "false"]):
        should_delete_ans = sys.argv[3] if len(sys.argv) == 4 else sys.argv[2]
        should_delete_pdfs = True if should_delete_ans.lower() == "true" else False
    merge_pdfs_from_directory(directory_path=directory, out_file_path=the_out_path, should_delete=should_delete_pdfs)
