import os
import tempfile
import uuid

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

from ocr_helper import extract_text

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("ID Card Reader")

uploaded_file = st.file_uploader("Upload an ID photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 1. Show the uploaded image
    st.image(uploaded_file, caption="Uploaded ID", use_container_width=True)

    # 2. Save temporarily and run OCR
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    with st.spinner("Reading text..."):
        text = extract_text(tmp_path)
    os.remove(tmp_path)

    # 3. Show the extracted text
    st.subheader("Extracted text")
    st.text_area("OCR result", text, height=300)



    
    # 4. Save to Supabase
    if st.button("Save scan to Supabase"):
        file_name = f"{uuid.uuid4()}{suffix}"
        supabase.storage.from_("id-images").upload(
            file_name,
            uploaded_file.getvalue(),
            {"content-type": uploaded_file.type},
        )
        supabase.table("id_scans").insert(
            {"extracted_text": text, "image_path": file_name}
        ).execute()
        st.success("Saved!")