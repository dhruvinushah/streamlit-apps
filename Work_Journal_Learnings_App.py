import streamlit as st
from datetime import datetime
import fitz  # PyMuPDF
import os
import subprocess

# Set page configuration
st.set_page_config(page_title="Work Journal", layout="centered")

# Title of the app
st.title("📘 Work Journal & Learnings")

# Description
st.markdown("Welcome to your personal work journal! Fill in the sections below to document your work activities and learnings. Once completed, your entry will be saved as a well-formatted PDF and automatically committed to your GitHub repository.")

# Input fields for journaling
journal_title = st.text_input("📝 What am I journaling?")
lesson_learned = st.text_area("📚 What was the lesson?")
how_to_do = st.text_area("🔧 How to do it?")
additional_notes = st.text_area("🗒️ Additional Notes (Optional)")

# Define the folder path for storing PDFs
folder_name = "Work Learnings"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Button to generate and save PDF
if st.button("Save and Commit to GitHub"):
    if journal_title and lesson_learned and how_to_do:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sanitized_title = journal_title.replace(' ', '_')
        pdf_filename = f"{sanitized_title}_{timestamp}.pdf"
        pdf_path = os.path.join(folder_name, pdf_filename)

        # Check for duplicate filename
        if os.path.exists(pdf_path):
            st.error("A journal entry with this title and timestamp already exists.")
        else:
            # Create PDF content
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

            # Generate PDF
            doc = fitz.open()
            page = doc.new_page()
            text_rect = fitz.Rect(50, 50, 550, 800)
            page.insert_textbox(text_rect, content, fontsize=12, fontname="helv")
            doc.save(pdf_path)
            doc.close()

            # Validate PDF was saved
            if os.path.exists(pdf_path):
                try:
                    # Git add, commit, and push
                    subprocess.run(["git", "add", pdf_path], check=True)
                    commit_message = f"Add journal entry: {pdf_filename}"
                    subprocess.run(["git", "commit", "-m", commit_message], check=True)
                    subprocess.run(["git", "push"], check=True)
                    st.success(f"✅ Your journal entry has been saved and committed to GitHub as '{pdf_filename}'")
                except subprocess.CalledProcessError as e:
                    st.error(f"❌ Git operation failed: {e}")
            else:
                st.error("❌ Failed to save the PDF file.")
    else:
        st.error("Please fill in all required fields before saving.")
