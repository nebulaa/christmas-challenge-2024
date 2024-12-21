import streamlit as st
import os
import re
from cryptography.fernet import Fernet


def sanitize(fileprefix):
    fileprefix = re.sub(r'[\\/:*?"<>|]', "", fileprefix)
    return fileprefix[:100] if len(fileprefix) > 100 else fileprefix


def check_file_extension(filename):
    try:
        file_ext = filename.rsplit(".", 1)[1].lower()
        fileprefix = filename.rsplit(".", 1)[0]
    except IndexError:
        st.error("Invalid file format.")
        return False, "", ""

    valid_extensions = {
        "jpg",
        "jpeg",
        "png",
        "gif",
        "pdf",
        "txt",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "mp3",
        "mp4",
        "avi",
        "mov",
        "wmv",
        "wav",
        "flac",
        "ogg",
        "m4a",
        "mkv",
        "webm",
        "mpg",
        "mpeg",
        "3gp",
        "flv",
        "svg",
        "bmp",
        "tiff",
        "webp",
        "json",
        "csv",
        "xml",
        "html",
        "md"
    }
    return (file_ext in valid_extensions), fileprefix, file_ext


def get_fernet_key():
    private_key_path = "private_key/fernet.key"
    if os.path.exists(private_key_path):
        with open(private_key_path, "rb") as f:
            fernet_key = f.read()
    else:
        fernet_key = Fernet.generate_key()
        os.makedirs("private_key", exist_ok=True)
        with open(private_key_path, "wb") as f:
            f.write(fernet_key)

    return fernet_key


def encrypt_file(file_bytes, fernet_key):
    fernet = Fernet(fernet_key)
    encrypted_file = fernet.encrypt(file_bytes)
    return encrypted_file


def save_file(uploaded_file, file_path):
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.success(f"File saved as {os.path.basename(file_path)}")


def save_file_encrypted(uploaded_file, file_path):
    temp_path = "temp_file"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    with open(temp_path, "rb") as f:
        file_bytes = f.read()

    fernet_key = get_fernet_key()
    encrypted_file = encrypt_file(file_bytes, fernet_key)

    with open(file_path, "wb") as encrypted_file_path:
        encrypted_file_path.write(encrypted_file)

    os.remove(temp_path)

    st.success(f"File encrypted and saved as {os.path.basename(file_path)}")


def decrypt_file(encrypted_file_data):
    fernet_key = get_fernet_key()
    fernet = Fernet(fernet_key)
    try:
        decrypted_data = fernet.decrypt(encrypted_file_data)
        return decrypted_data
    except Exception as e:
        st.error(f"Decryption failed: {e}")
        return None
