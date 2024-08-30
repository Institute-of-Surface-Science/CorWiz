import streamlit as st

st.markdown("# Data Protection")

# Read the markdown file
with open("dataprotection.md", "r", encoding="utf-8") as file:
    imprint_content = file.read()

# Display the content of the markdown file
st.markdown(imprint_content)