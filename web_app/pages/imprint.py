import streamlit as st

st.markdown("# Disclaimer/Imprint")

# Read the markdown file
with open("imprint.md", "r", encoding="utf-8") as file:
    imprint_content = file.read()

# Display the content of the markdown file
st.markdown(imprint_content)