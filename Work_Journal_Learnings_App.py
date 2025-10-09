import streamlit as st
from datetime import datetime
from fpdf import FPDF
import base64

st.set_page_config(page_title="Work Journal", layout="centered")
st.title("📘 Work Journal & Learnings")
st.markdown(
    "Welcome to your personal work journal! Fill in the sections below to document your work activities and learnings. "
    "Once completed, your entry will be saved as a well-formatted PDF and made available for download."
)

journal_title = st.text_input("📝 What am I journaling?")
lesson_learned = st.text_area("📚 What was the lesson?")
how_to_do = st.text_area("🔧 How to do it?")
additional_notes = st.text_area("🗒️ Additional Notes (Optional)")

if st.button("Save Entry"):
    if journal_title and lesson_learned and how_to_do:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sanitized_title = journal_title.replace(' ', '_')
        pdf_filename = f"{sanitized_title}_{timestamp}.pdf"

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        pdf.cell(0, 10, "Work Journal Entry", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(0, 10, f"Title: {journal_title}", ln=True)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"What was the lesson?\n{lesson_learned}")
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"How to do it?\n{how_to_do}")
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Additional Notes\n{additional_notes if additional_notes else 'N/A'}")

        # Output PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'data:application/pdf;base64,{b64}📥 Click here to download your journal entry</a>'

        st.success("✅ Your journal entry has been saved.")
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("❌ Please fill in all required fields before saving.")
