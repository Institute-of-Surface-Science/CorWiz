import streamlit as st

from helper import display_logo


def setup_footer(footer_container):
    with footer_container:
        left_column, middle_column, right_column = st.columns((0.75, 2.5, 1))
        with left_column:
            # optimized for 16:10
            empty_box_left, left_button_col, right_button_col, empty_box_right = st.columns((0.05, 0.75, 1.5, 1.25))


            with left_button_col:
                # center vertically (doesn't work with st.html)
                st.markdown("<div style='display: flex; align-items: center; height: 100%; justify-content: center;'>",
                            unsafe_allow_html=True)

                if st.button("Imprint"):
                    st.switch_page("pages/imprint.py")
                st.markdown("</div>", unsafe_allow_html=True)

            with right_button_col:
                # center vertically (doesn't work with st.html)
                st.markdown("<div style='display: flex; align-items: center; height: 100%; justify-content: center;'>",
                            unsafe_allow_html=True)
                if st.button("Data Protection"):
                    st.switch_page("pages/data_protection.py")
                st.markdown("</div>", unsafe_allow_html=True)

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
                    width="80%",
                    alt_text="Logo of the Helmholtz Metadata Colaboration www.helmholtz-metadaten.de",
                )

            with logo_nfdi4ing:
                display_logo(
                    url="https://www.nfdi4ing.de",
                    img_src="./app/static/logos/nfdi4ing.png",
                    width="80%",
                    alt_text="Logo of the German National Research Data Infrastructure for Engineering Sciences www.nfdi4ing.de",
                )
