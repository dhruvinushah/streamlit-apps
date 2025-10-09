import streamlit as st
from datetime import datetime
import fitz  # PyMuPDF
import base64

# Set page configuration
st.set_page_config(page_title="Work Journal", layout="centered")

# Title of the app
st.title("📘 Work Journal & Learnings")

# Description
st.markdown("Welcome to your personal work journal! Fill in the sections below to document your work activities and learnings. Once completed, your entry will be saved as a well-formatted PDF and made available for download.")

# Input fields for journaling
journal_title = st.text_input("📝 What am I journaling?")
lesson_learned = st.text_area("📚 What was the lesson?")
how_to_do = st.text_area("🔧 How to do it?")
additional_notes = st.text_area("🗒️ Additional Notes (Optional)")

# Button to generate and save PDF
if st.button("Save Entry"):
    if journal_title and lesson_learned and how_to_do:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sanitized_title = journal_title.replace(' ', '_')
        pdf_filename = f"{sanitized_title}_{timestamp}.pdf"

        # Create PDF content
        content = f"""Work Journal Entry
------------------

Title: {journal_title}

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

What was the lesson?
---------------------
{lesson_learned}

How to do it?
--------------
{how_to_do}

Additional Notes
----------------
{additional_notes if additional_notes else 'N/A'}
"""

        # Generate PDF in memory
        doc = fitz.open()
        page = doc.new_page()
        text_rect = fitz.Rect(50, 50, 550, 800)
        page.insert_textbox(text_rect, content, fontsize=12, fontname="helv", align=0)
        pdf_bytes = doc.write()
        doc.close()

        # Encode PDF for download
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64 here to download your journal entry</a>'
        st.success("✅ Your journal entry has been saved.")
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("Please fill in all required fields before saving.")
