import streamlit as st

from header import add_header
from footer import add_footer
from model_view import display_model_view

add_header()

model_view_container = st.container()
display_model_view(model_view_container)
add_footer()
