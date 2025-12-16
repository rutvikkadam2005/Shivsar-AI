# from fpdf import FPDF

# def txt_to_pdf(txt_path, pdf_path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=10)
    
#     pdf.set_font("Courier", size=11)  # Built-in font (safe)

#     with open(txt_path, "r", encoding="utf-8") as file:
#         for line in file:
#             try:
#                 # Encode to ascii (remove unsupported chars), then decode back to string
#                 safe_line = line.encode("ascii", errors="ignore").decode().strip()
#                 pdf.multi_cell(0, 8, safe_line)
#             except Exception as e:
#                 print(f"⚠️ Skipped line due to error: {e}")

#     pdf.output(pdf_path)
#     print(f"✅ PDF saved to: {pdf_path}")

# if __name__ == "__main__":
#     txt_to_pdf("shivsar_content.txt", "shivsar_export.pdf")
