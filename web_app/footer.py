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
        left_column, middle_column, right_column = st.columns((0.75, 2.5, 1))
        with left_column:
            # optimized for 16:10
            empty_box_left, left_button_col, right_button_col, empty_box_right = st.columns((0.05, 1.5, 1.9, 1.25))


            with left_button_col:
                st.markdown(
                    """
                    <div style='display: flex; align-items: center; justify-content: center; height: 100%; padding: 10px 0;'>
                        <a href='/imprint' target='_self' style='display: flex; align-items: center; justify-content: center;'>
                            <img src='./app/static/buttons/imprint.png' alt='Imprint' style='width: auto; height: 50px;'>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right_button_col:
                st.markdown(
                    """
                    <div style='display: flex; align-items: center; justify-content: center; height: 100%; padding: 10px 0;'>
                        <a href='/data_protection' target='_self' style='display: flex; align-items: center; justify-content: center;'>
                            <img src='./app/static/buttons/data_protection.png' alt='Data Protection' style='width: auto; height: 50px;'>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with right_column:
            logo_hereon, logo_hmc, logo_nfdi4ing = st.columns((1, 1, 1))

            with logo_hereon:
                display_logo(
                    url="https://www.hereon.de",
                    img_src="./app/static/logos/hereon.png",
                    width="80%",
                    alt_text="Logo of the Helmholtz Center hereon www.hereon.de",
                )

            with logo_hmc:
                display_logo(
                    url="https://www.helmholtz-metadaten.de",
                    img_src="./app/static/logos/hmc.png",
                    width="100%",
                    alt_text="Logo of the Helmholtz Metadata Colaboration www.helmholtz-metadaten.de",
                )

            with logo_nfdi4ing:
                display_logo(
                    url="https://www.nfdi4ing.de",
                    img_src="./app/static/logos/nfdi4ing.png",
                    width="80%",
                    alt_text="Logo of the German National Research Data Infrastructure for Engineering Sciences www.nfdi4ing.de",
                )
