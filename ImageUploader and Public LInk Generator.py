import streamlit as st
from pathlib import Path

# Title
st.title("Image Uploader and Public Link Generator")

# Create uploads folder
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Read query params
params = st.experimental_get_query_params()
image_key = params.get("image", [""])[0]

if image_key:
    # Show the image for the given key
    file_path = UPLOAD_DIR / image_key
    if file_path.exists():
        st.image(file_path.read_bytes(), caption=f"Image: {image_key}")
    else:
        st.error(f"Image '{image_key}' not found on the server.")

    # Show relative link that you can append to your host for public access
    st.markdown(f"""Your image is available at the relative link:  
    `?image={image_key}`  
    Once deployed to a public host, prepend the host to this:  
    `https://<your-host>/?image={image_key}`""")
    st.markdown("---")
    st.write("Upload another image:")
    uploaded = st.file_uploader("", type=["png", "jpg", "jpeg", "gif"])
    if uploaded:
        file_name = uploaded.name
        with open(UPLOAD_DIR / file_name, "wb") as f:
            f.write(uploaded.getbuffer())
        st.experimental_set_query_params(image=file_name)
        st.experimental_rerun()
else:
    # If no query param, show uploader
    uploaded = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "gif"])
    if uploaded is not None:
        file_name = uploaded.name
        with open(UPLOAD_DIR / file_name, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success(f"Saved file: {file_name}")
        st.image(uploaded, caption="Uploaded image")
        st.experimental_set_query_params(image=file_name)
        st.markdown(f"Click here or bookmark `?image={file_name}` to view your image.")
