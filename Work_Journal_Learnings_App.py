import streamlit as st
from datetime import datetime
import fitz  # PyMuPDF
import os

# Set page configuration
st.set_page_config(page_title="Work Journal", layout="centered")

# Title of the app
st.title("📘 Work Journal & Learnings")

# Description
st.markdown("Welcome to your personal work journal! Fill in the sections below to document your work activities and learnings. Once completed, you can save your entry as a well-formatted PDF for future reference.")

# Input fields for journaling
journal_title = st.text_input("📝 What am I journaling?")
lesson_learned = st.text_area("📚 What was the lesson?")
how_to_do = st.text_area("🔧 How to do it?")
additional_notes = st.text_area("🗒️ Additional Notes (Optional)")

# Button to generate and save PDF
if st.button("Save as PDF"):
    if journal_title and lesson_learned and how_to_do:
        content = f"""
        Work Journal Entry
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

        pdf_filename = f"{journal_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(".", pdf_filename)
        doc = fitz.open()
        page = doc.new_page()
        text_rect = fitz.Rect(50, 50, 550, 800)
        page.insert_textbox(text_rect, content, fontsize=12, fontname="helv")
        doc.save(pdf_path)
        doc.close()

        st.success(f"Your journal entry has been saved as {pdf_filename}")
        st.markdown(f"./{pdf_filename}")
    else:
        st.error("Please fill in all required fields before saving.")
