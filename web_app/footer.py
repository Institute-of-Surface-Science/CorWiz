import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space

from helper import display_logo

def add_footer():
    with st.container():
        add_vertical_space(20)

    footer_container = stylable_container(key="footer-box", css_styles="""{background-color: white}""")
    setup_footer(footer_container)


def setup_footer(footer_container):
    with footer_container:
        left_column, middle_column, right_column = st.columns((1, 1, 1))
        with left_column:
            st.write("impressum     data notice")
            # st.page_link("impressum")
            # st.page_link("data notice")
        with right_column:
            logo1, logo2, logo3 = st.columns((1, 1, 1))

            with logo1:
                display_logo(
                    url="https://www.hereon.de",
                    img_src="./app/static/logos/hereon.png",
                    width="80%",
                    alt_text="Logo of the Helmholtz Center hereon www.hereon.de",
                )

            with logo2:
                display_logo(
                    url="https://www.helmholtz-metadaten.de",
                    img_src="./app/static/logos/hmc.png",
                    width="100%",
                    alt_text="Logo of the Helmholtz Metadata Colaboration www.helmholtz-metadaten.de",
                )

            with logo3:
                display_logo(
                    url="https://www.nfdi4ing.de",
                    img_src="./app/static/logos/nfdi4ing.png",
                    width="80%",
                    alt_text="Logo of the German National Research Data Infrastructure for Engineering Sciences www.nfdi4ing.de",
                )
