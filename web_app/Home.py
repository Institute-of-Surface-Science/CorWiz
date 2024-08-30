import streamlit as st

from header import add_header
from footer import add_footer
from model_view import display_model_view
from helper import local_css

st.set_page_config(page_title="CorWiz", page_icon=":material/rainy:", layout="wide", initial_sidebar_state="auto")

local_css('style/style.css')

add_header()

model_view_container = st.container()
display_model_view(model_view_container)

add_footer()
