import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from helper import display_logo

def add_header():
    header_container = st.container()
    setup_header(header_container)


def setup_header(header_container):
    with header_container:
        with st.container(height=150, border=False):
            left_column, middle_column, right_column = st.columns((3, 3, 3))
            with left_column:
                with stylable_container(key="logo_box",
                                        css_styles="""{background-color: white; border-radius: 0.5rem;padding: 2px;padding-left:10px;padding-right:10px;max-height:150px;box-sizing: border-box;}"""):
                    display_logo(
                        url="http://corwiz.xyz/",
                        img_src="./app/static/logos/corwiz.png",
                        width="90%",
                        alt_text="Logo of Corwiz",
                    )
            with right_column:
                display_logo(
                    url="http://corwiz.xyz/",
                    img_src="./app/static/logos/banner_small.gif",
                    width="90%",
                    alt_text="Animated Banner",
                )
