import streamlit as st
import requests

st.title("Customer Inquiry Triage (Bonus Challenges included)")

message = st.text_area("Enter Customer Message (optional if uploading a file):")
file = st.file_uploader("Or upload a file (PDF or Image)")

if st.button("Classify"):
    files = {"file": file} if file else None
    data = {"message": message}

    response = requests.post("http://localhost:8000/triage", data=data, files=files)

    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error processing request.")
