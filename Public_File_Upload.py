import streamlit as st
import os
from process_file import check_file_extension, sanitize, save_file

st.title("Web Server Coding Challenge")
st.subheader("Upload a public file")

upload_public = st.checkbox("Check to upload a public file")
if upload_public:
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    uploaded_file = st.file_uploader("Upload a file")
    with st.spinner("Uploading file..."):
        if uploaded_file is not None:
            original_file_name = uploaded_file.name
            is_valid_extension, fileprefix, file_ext = check_file_extension(original_file_name)

            if is_valid_extension:
                sanitized_file_name = sanitize(fileprefix) + "." + file_ext
                file_path = os.path.join(uploads_dir, sanitized_file_name)
                save_file(uploaded_file, file_path)
            else:
                st.error("Unsupported file extension. Please upload a file with a valid extension.")

