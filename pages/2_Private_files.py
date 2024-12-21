import streamlit as st
import os
import sqlite3
from authenticate import check_password
from process_file import check_file_extension, sanitize, save_file_encrypted

st.title("Private File Uploader")

if not check_password():
    st.stop()

def add_file_key(file_name, key):
    with sqlite3.connect('sqldb.db', check_same_thread=False) as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS filekeys (
                file_name TEXT PRIMARY KEY,
                key TEXT
            )
            """
        )
        try:
            cursor.execute(
                "INSERT INTO filekeys (file_name, key) VALUES (?, ?)",
                (file_name, key),
            )
            db_conn.commit()
        except sqlite3.IntegrityError:
            st.error("This file already exists. Please upload a different file.")
            return False
        except sqlite3.OperationalError as e:
            st.error(f"An error occurred while adding the file key: {e}")
            return False
    return True


uploads_dir = "private_uploads"
os.makedirs(uploads_dir, exist_ok=True)

user_file_passkey = st.text_input("Enter a password to secure your new file upload", max_chars=10)
if user_file_passkey:
    uploaded_file = st.file_uploader("Upload a file")
    with st.spinner("Uploading file..."):
        if uploaded_file is not None:
            original_file_name = uploaded_file.name
            is_valid_extension, fileprefix, file_ext = check_file_extension(original_file_name)

            if is_valid_extension:
                sanitized_file_name = sanitize(fileprefix) + "." + file_ext
                file_path = os.path.join(uploads_dir, sanitized_file_name)
                result = add_file_key(sanitized_file_name, user_file_passkey)
                if result:
                    save_file_encrypted(uploaded_file, file_path)
                else:
                    st.error("File not saved. Please try again.")
                st.success("File key added successfully. Encrypted file saved.")
            else:
                st.error("Unsupported file extension. Please upload a different file.")


