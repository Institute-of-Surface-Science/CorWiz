import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Corwiz", page_icon=":woman_scientist:", layout="wide")


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

with header:
    left_column, right_column = st.columns((8, 1))
    with left_column:
        st.title("CorWiz - A web service to assist engineers in accessing and utilizing data on steel corrosion.")
        st.subheader("Developed by Aravinth Ravikumar, Dr.Sven Berger and Dr. Daniel Höche")
        st.write(
            "The goal is to create a comprehensive database of corrosion knowledge, including both structured and unstructured data such as research articles. Currently, engineers face challenges in selecting appropriate models and accessing relevant data for corrosion simulations. CorWiz aims to address this by providing a user-friendly web tool that offers engineers access to corrosion data, models, and relevant literature. By inputting parameters such as substrate material and environmental conditions, users can obtain corrosion grades, simulation results, and other structured data. The development of CorWiz involves data scraping, processing, and quality assessment, which will be facilitated by tools developed for the Kadi4Mat research data management platform. This project aims to streamline the design process, raise awareness of potential corrosion issues, and contribute to more cost-effective and eco-friendly design practices.")
        st.write("[Learn more at >](https://www.hereon.de/institutes/surface_science/projects/112600/index.php.en)")
    with right_column:
        st_lottie(lottie_animation, height=100, key="coding")

with main_app:
    st.write("---")
    st.header("Corrosion Mass Loss Model")

    # Extract the model names and identifiers from the excel sheet atmospheric_corrosion_model_kadi_identifiers.xlsx
    # atmospheric_corrosion_model_kadi_identifiers = pd.read_excel('../data/atmospheric_corrosion_model_kadi_identifiers.xlsx')
    # model_names = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 0].tolist()
    # model_ids = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 1].tolist()
    # model_kadi_identifiers = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 2].tolist()
    # model_developers = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 3].tolist()
    # model_abstracts = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 4].tolist()
    # model_special_notes = atmospheric_corrosion_model_kadi_identifiers.iloc[:, 5].tolist()
    #
    # model = st.selectbox(
    #     'Please select model',
    #     ((model_names))
    # )
    # model_identifier = model_kadi_identifiers[model_names.index(model)]
    # model_id =  model_ids[model_names.index(model)]
    # st.subheader("Selected model: " + model)
    # model_record = manager.record(identifier=model_identifier)
    # st.write("[Model in Kadi4mat](https://a1sv2300300.fzg.local/records/" + str(model_record.id) + ")")
    # Download the tables associated with model record if any
    # try:
    #     table_id = model_record.get_file_id('tables.xlsx')
    #     model_record.download_file(table_id, '../data/temp/tables.xlsx')
    # except Exception as err:
    #     pass

    image_column, data_column, = st.columns((2, 1))

    with data_column:
        st.write("test")
        # st.write("Model developed by: " + model_developers[model_names.index(model)])
        # st.write("Model Abstract: " + model_abstracts[model_names.index(model)])
        # st.write("Model Notes: " + model_special_notes[model_names.index(model)])

        # if model_id == 1:
        #     with st.container():
        #         # table_2 = pd.read_excel('../data/temp/tables.xlsx', sheet_name='Table_2', header=None, engine='openpyxl')
        #         # table_4 = pd.read_excel('../data/temp/tables.xlsx', sheet_name='Table_4', header=None, engine='openpyxl')
        #         atmosphere_types = table_4.iloc[0, 1:]
        #         atmosphere_types['4'] = "Enter Cl^- and SO_2 pollution annual averages"
        #         atmosphere_types = atmosphere_types.to_list()
        #         binary_interaction = st.selectbox(
        #         'Use Binary Interaction?',
        #         ((True, False,))
        #         )
        #
        #         atmosphere = st.selectbox(
        #         'Select atmosphere:',
        #         ((atmosphere_types))
        #         )
        #         Cl = table_2.iloc[7, 2]
        #         SO2 = table_2.iloc[7, 2]
        #         atmosphere = atmosphere_types.index(atmosphere)
        #         if atmosphere == 3:
        #             Cl = float(st.text_input(r"$Cl^-$ - chloride pollution annual average  $[mg Cl^{-} dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
        #             SO2 = float(st.text_input(r"$SO_2$ - SO2 pollution annual average  $[mg SO_2 dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
        #         annual_corrosion = float(st.text_input(r"$A$ - Corrosion after the first year of exposure [um]", str(table_2.iloc[8, 2])))
        #         temp = float(st.text_input(r"$T$ - Temperature [°C]", str(table_2.iloc[6, 2])))
        #         tw = float(st.text_input(r"$T_w$ - Wetness time [annual fraction]", str(table_2.iloc[4, 2])))
        #         D = float(st.text_input(r"$D$ - Number of rainy days per year [days]", str(table_2.iloc[5, 2])))
        #
        #         if binary_interaction:
        #             st.write(r'Annual corrosion, A $[um]$ = $132.4Cl^-(1 + 0.038T - 1.96t_w - 0.53SO_2 + 74.6t_w(1 + 1.07SO_2) - 6.3)$ ')
        #         else:
        #             st.write(r'Annual corrosion, A $[um]$ = $33.0 + 57.4Cl^- + 26.6SO_2$')
        #
        #         st.write(r'Exponent, n = $0.570 + 0.0057Cl^-T + 7.7 \times 10^{-4}D - 1.7 \times 10^{-3}A$')
        #
        #         model = i_the_prediction_of_atmospheric_corrosion_from_met(binary_interaction, atmosphere, parameters=[Cl, SO2, temp, tw, D])
        #
        # time = float(st.text_input(r"$t$ - The exposure time, in [years]", "0.1"))
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

