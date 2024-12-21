import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer

st.title("Public Files - Download Links")

uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

show_download_links = st.checkbox("Show download links")
if show_download_links:

    if os.path.exists(uploads_dir):
        for file_name in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.download_button(
                        label=f"{file_name}",
                        data=file_bytes,
                        file_name=file_name,
                    )
    else:
        st.write("Uploads directory does not exist. Please upload a file.")

preview = st.checkbox("Preview files")
if preview:

    image_file_extension = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
    audio_file_extension = ["mp3", "wav", "ogg", "flac"]
    video_file_extension = ["mp4", "avi", "mov", "wmv", "mkv", "webm"]
    text_file_extension = ["txt", "json", "csv", "xml", "html"]
    
    selected_file = st.selectbox("Select a file", os.listdir(uploads_dir))
    if selected_file:
        file_path = os.path.join(uploads_dir, selected_file)
        if os.path.isfile(file_path):
            if selected_file.rsplit(".", 1)[1].lower() in image_file_extension:
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.image(file_bytes)
            elif selected_file.rsplit(".", 1)[1].lower() in audio_file_extension:
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.audio(file_bytes)
            elif selected_file.rsplit(".", 1)[1].lower() in video_file_extension:
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.video(file_bytes)
            elif selected_file.rsplit(".", 1)[1].lower() == "pdf":
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    pdf_viewer(file_bytes)
            elif selected_file.rsplit(".", 1)[1].lower() == "md":
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.markdown(file_bytes)
            elif selected_file.rsplit(".", 1)[1].lower() in text_file_extension:
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    st.code(file_bytes, wrap_lines=True)
            else:
                st.error("Unsupported file format. Unable to preview.")
    else:
        st.write("Uploads directory does not exist. Please upload a file.")