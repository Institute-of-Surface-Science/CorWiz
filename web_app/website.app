import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

st.set_page_config(page_title="Corwiz Website Prototype", page_icon=":woman_scientist:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---- LOAD ASSETS ----
lottie_animation = load_lottieurl("https://lottie.host/06c2ad3e-b44f-431c-ac89-4c4b916c4b43/b4ZvbBJBa9.json")



# ---- HEADER SECTION ----

with st.container():
    left_column, right_column = st.columns((8, 1))
    with left_column:
        st.subheader("CORWIZ - A web service being developed to assist engineers in accessing and utilizing data on steel corrosion.")
        st.title("Developed by Aravinth Ravikumar, Dr.Sven Berger and Dr. Daniel Höche")
        st.write("The goal is to create a comprehensive database of corrosion knowledge, including both structured and unstructured data such as research articles. Currently, engineers face challenges in selecting appropriate models and accessing relevant data for corrosion simulations. CorWiz aims to address this by providing a user-friendly web tool that offers engineers access to corrosion data, models, and relevant literature. By inputting parameters such as substrate material and environmental conditions, users can obtain corrosion grades, simulation results, and other structured data. The development of CorWiz involves data scraping, processing, and quality assessment, which will be facilitated by tools developed for the Kadi4Mat research data management platform. This project aims to streamline the design process, raise awareness of potential corrosion issues, and contribute to more cost-effective and eco-friendly design practices.")
        st.write("[Learn more at >](https://www.hereon.de/institutes/surface_science/projects/112600/index.php.en)")
    with right_column:    
        st_lottie(lottie_animation, height=100, key="coding")


# --- MAIN PART ----

with st.container():
    st.write("---")
    st.header("Corrosion Mass Loss Model")
    st.subheader("Standard: ISO 9224:2012")
    st.write("[Download PDF >](https://a1sv2300300.fzg.local/records/44?tab=files)")

    data_column, image_column = st.columns((1, 1))

    with data_column:
        st.write("$D$ - Mass loss [grams]")

        st.write("Short term mass loss:")
        st.image(Image.open("../bin/images/iso_9224_eqn.png"), width=250)
        st.write("Long term mass loss (> 20 years):")
        st.image(Image.open("../bin/images/iso_9224_eqn_2.png"), width=300)

        corrosion_rate = float(st.text_input("$r_{corr}$ - The corrosion rate in the first year, expressed in grams per square meter per year [g/(m²⋅a)]", "0"))
        time = float(st.text_input("$t$ - The exposure time, in [years]", "0.1"))
        b = float(st.text_input("$b$ - Time exponent specific to the metal and environment (usually less than one)", "0.1"))

        t = np.linspace(0, time, 400)
        if time<=20:
            D = b * corrosion_rate * t**(b - 1)
            plt.figure(figsize=(10, 6))
            plt.plot(t, D, label=f'D = {b:.2f} * {corrosion_rate:.2f} * t^({b:.2f}-1)', color='blue')
            plt.xlabel('Time (years)')
            plt.ylabel('D')
            plt.title('Plot of D = b*r*t^(b-1)')
            plt.legend()
            plt.grid(True)

            # Save the figure
            plt.savefig('../bin/images/plot_output.png')

        else:
            D = corrosion_rate*(20**b + b*(20**(b-1))*(t-20))
            plt.figure(figsize=(10, 6))
            plt.plot(t, D, label=f'D = {b:.2f} * {corrosion_rate:.2f} * t^({b:.2f}-1)', color='blue')
            plt.xlabel('Time (years)')
            plt.ylabel('D')
            plt.title('Plot of D = b*r*t^(b-1)')
            plt.legend()
            plt.grid(True)

            # Save the figure
            plt.savefig('../bin/images/plot_output.png')

    with image_column:
        st.image(Image.open("../bin/images/plot_output.png"))