import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
from models import model1, model2

st.set_page_config(page_title="Corwiz", page_icon=":woman_scientist:", layout="wide", initial_sidebar_state="collapsed")


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
                            css_styles="""{
                                            background-color: white
                                          }
                                          """)


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


with header:
    left_column, right_column = st.columns((8, 1))
    with left_column:
        st.title("CorWiz - A web service to assist engineers in accessing and utilizing data on steel corrosion.")
        st.subheader("Developed by Aravinth Ravikumar, Dr.Sven Berger and Dr. Daniel Höche")
        st.write(
            "The goal is to create a comprehensive database of corrosion knowledge, including both structured and unstructured data such as research articles. Currently, engineers face challenges in selecting appropriate models and accessing relevant data for corrosion simulations. CorWiz aims to address this by providing a user-friendly web tool that offers engineers access to corrosion data, models, and relevant literature. By inputting parameters such as substrate material and environmental conditions, users can obtain corrosion grades, simulation results, and other structured data. The development of CorWiz involves data scraping, processing, and quality assessment, which will be facilitated by tools developed for the Kadi4Mat research data management platform. This project aims to streamline the design process, raise awareness of potential corrosion issues, and contribute to more cost-effective and eco-friendly design practices.")
        st.write("[Learn more at >](https://www.hereon.de/institutes/surface_science/projects/112600/index.php.en)")
    with right_column:
        # st_lottie(lottie_animation, height=100, key="coding")
        # st.image('../data/animations/Presentation2v2.gif')
        display_logo(
            url="https://www.http://corwiz.xyz/",
            img_src="./app/static/logos/Presentation2v2.gif",
            width="80%",
            alt_text="Logo of Corwiz",
        )

with main_app:
    st.write("---")
    st.header("Corrosion Mass Loss Model")

    # Extract the model names and identifiers from the excel sheet atmospheric_corrosion_model_kadi_identifiers.xlsx
    # atmospheric_corrosion_model_kadi_identifiers = pd.read_excel('../data/atmospheric_corrosion_model_kadi_identifiers.xlsx')
    atmospheric_corrosion_model_kadi_identifiers = pd.read_csv('../data/atmospheric_corrosion_model_kadi_identifiers.csv')

    columns = ['model_names', 'model_ids', 'model_kadi_identifiers', 'model_developers', 'model_abstracts', 'model_special_notes']
    model_info = {col: atmospheric_corrosion_model_kadi_identifiers.iloc[:, idx].tolist() for idx, col in enumerate(columns)}
    
    model = st.selectbox(
        'Please select model',
        ((model_info['model_names']))
    )
    model_identifier = model_info['model_kadi_identifiers'][model_info['model_names'].index(model)]
    model_id =  model_info['model_ids'][model_info['model_names'].index(model)]
    st.subheader("Selected model: " + model)

    image_column, data_column, = st.columns((1, 1))

    with data_column:
        st.write("Model developed by: " + model_info['model_developers'][model_info['model_names'].index(model)])
        st.write("Model Abstract: " + model_info['model_abstracts'][model_info['model_names'].index(model)])
        try:
            st.write("Model Notes: " + model_info['model_special_notes'][model_info['model_names'].index(model)])
        except:
            pass

        if model_id == 1:
            with st.container():
                model = model1(model_identifier)

        elif model_id == 2:
            with st.container():
                model = model2(model_identifier)
        
        time = float(st.text_input(r"$t$ - The exposure time, in [years]", "0.1"))
        #
        # t = np.linspace(0, time, 400)
        # D = model.eval_material_loss(t)
        # plt.figure(figsize=(10, 6))
        # plt.plot(t, D, color='blue')
        # plt.xlabel(r'Time [years]')
        # plt.ylabel(r'Mass loss $[um]$')
        # plt.legend()
        # plt.grid(True)
        #
        # # Save the figure
        # plt.savefig('../data/images/plot_output.png')

    with image_column:
        st.image("../data/images/plot_output.png")

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

