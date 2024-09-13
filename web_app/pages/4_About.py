import os
import sys

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from header import add_header
from footer import add_footer
from helper import display_logo

add_header()

st.markdown("# About")

top_container = st.container()
bottom_container = st.container()

with top_container:
    info_column, funding_column = st.columns((1, 1))

    with info_column:
        st.markdown(
            "The goal is to create a comprehensive database of corrosion knowledge, including both structured and unstructured data such as research articles. "
            "Currently, engineers face challenges in selecting appropriate models and accessing relevant data for corrosion simulations."
            " CorWiz aims to address this by providing a user-friendly web tool that offers engineers access to corrosion data, models, and relevant literature."
            " By inputting parameters such as substrate material and environmental conditions, users can obtain corrosion grades, simulation results, and other structured data."
            " The development of CorWiz involves data scraping, processing, and quality assessment, which will be facilitated by tools developed for the Kadi4Mat research data management platform."
            " This project aims to streamline the design process, raise awareness of potential corrosion issues, and contribute to more cost-effective and eco-friendly design practices.")
        st.markdown("[Learn more at >](https://www.hereon.de/institutes/surface_science/projects/112600/index.php.en)")

    with funding_column:
        st.markdown("## Funding")
        st.markdown("### CorWiz")
        st.markdown("The implementation of CorWiz was funded through a seed fund grant from NFDI4Ing:")
        display_logo(
            url="https://www.nfdi4ing.de",
            img_src="./app/static/logos/nfdi4ing.png",
            width="80%",
            alt_text="Logo of the German National Research Data Infrastructure for Engineering Sciences www.nfdi4ing.de",
        )
        st.markdown("### MetaSurf")
        display_logo(
            url="www.corwiz.xyz",
            img_src="./app/static/logos/metasurf.png",
            width="80%",
            alt_text="Logo of the Helmholtz Metadata Colaboration Project MetaSurf",
        )
        st.markdown("Further development of data gathering and creating a data repository is funded through the HMC project \"MetaSurf\":")
        display_logo(
            url="https://www.helmholtz-metadaten.de",
            img_src="./app/static/logos/hmc.png",
            width="80%",
            alt_text="Logo of the Helmholtz Metadata Colaboration www.helmholtz-metadaten.de",
        )
with bottom_container:
    author_column, cite_column = st.columns((1, 1))
    with author_column:
        st.markdown("## Authors")

        st.markdown("### Responsible Ph.D. Student: Aravinth Ravikumar, M.Sc.")
        aravinth = st.container()

        with aravinth:
            st.markdown("![Aravinth](./app/static/pictures/aravinth.jpg)")
            cv=st.expander("CV")
            with cv:
                with open("cv_aravinth.md", "r", encoding="utf-8") as file:
                    cv = file.read()

                # Display the content of the markdown file
                st.markdown(cv)

        st.markdown("### Project Lead: Dr. Sven Berger")
        sven = st.container()

        with sven:
            st.markdown("![Sven](./app/static/pictures/sven.jpg)")
            cv=st.expander("CV")
            with cv:
                with open("cv_sven.md", "r", encoding="utf-8") as file:
                    cv = file.read()

                # Display the content of the markdown file
                st.markdown(cv)

        st.markdown("### Department Head: Dr. Daniel Höche")
        daniel = st.container()

        with daniel:
            st.markdown("![Daniel](./app/static/pictures/daniel.jpg)")
            cv=st.expander("CV")
            with cv:
                with open("cv_daniel.md", "r", encoding="utf-8") as file:
                    cv = file.read()

                # Display the content of the markdown file
                st.markdown(cv)
    with cite_column:
        st.markdown("## Cite Us")
        st.markdown("Please cite the DOI: 10.5281/zenodo.13753842")

add_footer()
