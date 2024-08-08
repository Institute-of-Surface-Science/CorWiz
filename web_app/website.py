import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stylable_container import stylable_container

from models import model1, model2, model3, model4, model5, model6

st.set_page_config(page_title="CorWiz", page_icon=":material/rainy:", layout="wide", initial_sidebar_state="collapsed")

# TODO: move to local css file
st.markdown(
    f'''
       <style>
           .block-container {{
               padding-top: 2rem;
               padding-right: 1rem;
               padding-left: 1rem;
               padding-bottom: 2rem;
           }}
       </style>
           ''',
    unsafe_allow_html=True,
)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<\style>", unsafe_allow_html=True)


local_css('style/style.css')

lottie_animation = load_lottieurl("https://lottie.host/06c2ad3e-b44f-431c-ac89-4c4b916c4b43/b4ZvbBJBa9.json")

header = st.container()
main_app = st.container()
empty = st.container()
footer = stylable_container(key="footer-box",
                            css_styles="""{background-color: white}""")


def display_logo(url, img_src, alt_text, width="", height=""):
    height_html = ""
    if height:
        height_html = f"""max-height: {height} """

    width_html = ""
    if width:
        width_html = f"""width="{width}" """

    st.html(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; {height_html};">
            <a href="{url}" target="_blank">
                <img src="{img_src}" {width_html} alt="{alt_text}" style="{height_html};">
            </a>
        </div>
        """
    )


with header:
    with st.container(height=150, border=False):
        left_column, middle_column, right_column = st.columns((1, 5, 1))
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
                height="150px",
                alt_text="Animated Banner",
            )

with main_app:
    st.write("---")
    st.header("Corrosion Mass Loss Model")

    # Extract the model names and identifiers from the atmospheric_corrosion_model_kadi_identifiers.csv file

    atmospheric_corrosion_model_kadi_identifiers = pd.read_csv(
        '../data/atmospheric_corrosion_model_kadi_identifiers.csv')

    columns = ['model_names', 'model_ids', 'model_kadi_identifiers', 'model_developers', 'model_abstracts',
               'model_special_notes']
    model_info = {col: atmospheric_corrosion_model_kadi_identifiers.iloc[:, idx].tolist() for idx, col in
                  enumerate(columns)}

    model = st.selectbox(
        'Please select model',
        ((model_info['model_names']))
    )
    model_identifier = model_info['model_kadi_identifiers'][model_info['model_names'].index(model)]
    model_id = model_info['model_ids'][model_info['model_names'].index(model)]
    st.subheader("Selected model: " + model)

    image_column, data_column, = st.columns((1, 1))
    fig = plt.figure(figsize=(10, 6))

    with data_column:
        st.write("Model developed by: " + model_info['model_developers'][model_info['model_names'].index(model)])
        st.write("Model Abstract: " + str(model_info['model_abstracts'][model_info['model_names'].index(model)]))
        try:
            st.write("Model Notes: " + model_info['model_special_notes'][model_info['model_names'].index(model)])
        except:
            pass

        if model_id == 1:
            with st.container():
                model, time = model1(model_identifier)

        elif model_id == 2:
            with st.container():
                model, time = model2(model_identifier)

        elif model_id == 3:
            with st.container():
                model, time = model3(model_identifier)

        elif model_id == 4:
            with st.container():
                model, time = model4(model_identifier)

        elif model_id == 5:
            with st.container():
                model, time = model5(model_identifier)

        elif model_id == 6:
            with st.container():
                model, time = model6(model_identifier)

        t = np.linspace(0, time, 400)
        D = model.eval_material_loss(t)
        plt.plot(t, D, color='blue')
        plt.xlabel(r'Time [years]')
        plt.ylabel(r'Mass loss $[um]$')
        plt.legend()
        plt.grid(True)

    with image_column:
        # # Save the figure
        # plt.savefig('../data/images/plot_output.png')
        # st.image("../data/images/plot_output.png")
        st.pyplot(fig)

with empty:
    add_vertical_space(20)


def display_logo(url, img_src, width, alt_text):
    st.html(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
            <a href="{url}" target="_blank">
                <img src="{img_src}" width="{width}" alt="{alt_text}">
            </a>
        </div>
        """
    )


with footer:
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
                width="80%",
                alt_text="Logo of the Helmholtz Metadata Colaboration www.helmholtz-metadaten.de",
            )

        with logo3:
            display_logo(
                url="https://www.nfdi4ing.de",
                img_src="./app/static/logos/nfdi4ing.png",
                width="80%",
                alt_text="Logo of the German National Research Data Infrastructure for Engineering Sciences www.nfdi4ing.de",
            )
