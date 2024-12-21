import streamlit as st
import os
import sqlite3
from authenticate import check_password
from process_file import decrypt_file

st.title("Private File Downloads")

if not check_password():
    st.stop()

uploads_dir = "private_uploads"
list_files = st.checkbox("Show list of password-protected files")
if list_files:
    if os.path.exists(uploads_dir):
        st.subheader("List of password-protected files:")
        for file_name in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, file_name)
            if os.path.isfile(file_path):
                st.write(f"{file_name}")
    else:
        st.write("Uploads directory does not exist.")

file_name = st.selectbox("Select a file", os.listdir(uploads_dir))
file_passkey = st.text_input("Enter the file passkey")

if file_name and file_passkey:
    if file_name in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, file_name)
        if os.path.isfile(file_path):
            with sqlite3.connect('sqldb.db', check_same_thread=False) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute(
                    """
                    SELECT key FROM filekeys WHERE file_name = ?
                    """,
                    (file_name,),
                )
                result = cursor.fetchone()
                if result is not None and result[0] == file_passkey:
                    with open(file_path, "rb") as file:
                        encrypted_file = file.read()
                        decrypted_file = decrypt_file(encrypted_file)
                        if decrypted_file is not None:
                            st.download_button(
                                label=f"Download {file_name}",
                                data=decrypted_file,
                                file_name=file_name,
                            )
                else:
                    st.error("File passkey does not match.")
    else:
        st.error("File does not exist.")


