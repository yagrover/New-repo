import streamlit as st
import uuid
from textract_utils import upload_to_s3, extract_text_from_textract
from genai_utils import generate_dispute_reply

bucket_name = "invoicedisputedemo"  # 🪣 Replace with your bucket

st.set_page_config(page_title="Invoice Dispute Resolver")
st.title("📄 Invoice Dispute Resolution Assistant (Textract + Claude)")

# ✅ Always show the uploader
uploaded_file = st.file_uploader("📤 Upload a dispute email (PDF)", type=["pdf"])

# ✅ Check if a file is uploaded
if uploaded_file is not None:
    # Unique file key for S3
    file_key = f"uploads/{uuid.uuid4()}.pdf"

    st.info("⏫ Uploading to S3...")
    try:
        upload_to_s3(uploaded_file, bucket_name, file_key, st.secrets["aws"])
        st.success("✅ Uploaded successfully.")
    except Exception as e:
        st.error(f"❌ Upload failed: {e}")
        st.stop()

    st.info("🧾 Extracting text using Textract...")
    try:
        extracted_text = extract_text_from_textract(bucket_name, file_key, st.secrets["aws"])
        st.success("✅ Text extraction done.")
    except Exception as e:
        st.error(f"❌ Textract failed: {e}")
        st.stop()

    st.subheader("📄 Extracted PDF Content")
    st.text_area("Extracted Text", extracted_text, height=400)

    # ✅ Button to trigger Claude
    if st.button("🧠 Generate AI-Powered Reply"):
        with st.spinner("Generating draft reply using Claude 3 Haiku..."):
            try:
                reply = generate_dispute_reply(extracted_text)
                st.success("✅ Draft generated!")
                st.subheader("✉️ AI-Generated Reply")
                st.text_area("Reply", reply, height=300)
            except Exception as e:
                st.error(f"❌ Claude generation failed: {e}")
