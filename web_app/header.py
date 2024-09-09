import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from helper import display_logo
from helper import local_css

def add_header():
    st.set_page_config(page_title="CorWiz", page_icon=":material/rainy:", layout="wide", initial_sidebar_state="auto")
    local_css('style/style.css')

    header_container = st.container()
    setup_header(header_container)
    github_url = "https://github.com/Institute-of-Surface-Science/CorWiz"

    # Add the GitHub logo and link to the sidebar
    with st.sidebar:
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center;'>
                <a href="{github_url}" target="_blank">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40" alt="GitHub Repo">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )


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
