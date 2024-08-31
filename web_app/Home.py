import streamlit as st

from header import add_header
from footer import add_footer
from model_view import model_view

add_header()

model_view_container = st.container()
model_view(model_view_container)

add_footer()
