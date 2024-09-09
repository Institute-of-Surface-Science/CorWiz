import streamlit as st

from header import add_header
from footer import add_footer
from model_view import display_model_view
from measurement_view import display_measurement_view

add_header()

model_view_container = st.container()
display_model_view(model_view_container)

measurement_view_container = st.container()
display_measurement_view(measurement_view_container)

add_footer()
