import frappe
import os
import zipfile
from frappe.utils.pdf import get_pdf
from frappe.utils import get_files_path

@frappe.whitelist()
def download_multiple_pdfs(doctype, docnames, print_format=None):
    import json

    docnames = json.loads(docnames)
    files = []

    # Create individual PDFs
    for name in docnames:
        pdf_data = get_pdf(frappe.get_print(doctype, name, print_format))
        filename = f"{doctype}-{name}.pdf"
        file_path = os.path.join(get_files_path(), filename)

        with open(file_path, "wb") as f:
            f.write(pdf_data)
        files.append(file_path)

    # Create ZIP file
    zip_filename = "Multiple_Records_PDFs.zip"
    zip_path = os.path.join(get_files_path(), zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

    return {
        "file_url": f"/files/{zip_filename}",
        "filename": zip_filename
    }
