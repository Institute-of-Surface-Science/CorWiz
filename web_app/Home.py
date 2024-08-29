import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stylable_container import stylable_container

from header import setup_header
from footer import setup_footer
from model_view import model_view
from helper import local_css

st.set_page_config(page_title="CorWiz", page_icon=":material/rainy:", layout="wide", initial_sidebar_state="auto")

local_css('style/style.css')

header_container = st.container()
setup_header(header_container)

model_view_container = st.container()
model_view(model_view_container)

with st.container():
    add_vertical_space(20)


footer_container = stylable_container(key="footer-box", css_styles="""{background-color: white}""")
setup_footer(footer_container)
