import numpy as np
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import pandas as pd
import io
from measurements import *
from typing import Union, List

# Mapping from identifiers to their respective corrosion measurement classes

corwiz_measurements = {
    'exp_data_ali2020': Ali2020Measurement
}

# Keep track of all measurements added for plotting
plot_data = []

def display_measurement_info(measurement: Measurement) -> None:
    """Displays the measurement description and notes."""
    st.markdown(measurement.description)
    if measurement.special_note:
        st.markdown("#### Measurement Notes: \n" + measurement.special_note)


def generate_plot(measurements, current_measurement, time_range):
    """Generates and returns a Plotly Express figure for mass loss over time."""
    t = np.linspace(0, time_range, 400)

    # Initialize a list for plotting
    plot_df = []

    # Plot the current measurement's data first
    D = current_measurement.evaluate_material_loss(t)
    current_measurement_data = pd.DataFrame(
        {'Time': t, 'Mass Loss': D, 'Measurement': f"{current_measurement.measurement_name} (live)"})
    plot_df.append(current_measurement_data)

    # Collect all y-values to check for max/min difference for log scaling
    all_y_values = [D]

    # Plot the additional measurements
    measurement_counter = 1
    for measurement in measurements:
        D = measurement.evaluate_material_loss(t)
        measurement_data = pd.DataFrame({'Time': t, 'Mass Loss': D, 'Measurement': f"{measurement.measurement_name} ({measurement_counter})"})
        plot_df.append(measurement_data)
        all_y_values.append(D)
        measurement_counter += 1

    # Combine all data into a single DataFrame
    plot_df = pd.concat(plot_df)

    # Flatten the list of y-values to check the ratio between max/min values
    all_y_values_flat = np.concatenate(all_y_values)

    # Filter out non-positive values to avoid errors with log scaling
    positive_y_values = all_y_values_flat[all_y_values_flat > 0]

    # Determine whether to use a log scale
    if len(positive_y_values) > 0:
        max_value = np.max(positive_y_values)
        min_value = np.min(positive_y_values)
        yaxis_type = "log" if max_value / min_value > 100 else "linear"
    else:
        yaxis_type = "linear"

    px.defaults.template = "plotly_white"

    # Plot using Plotly Express and use 'Measurement' for distinct colors and labels
    fig = px.line(
        plot_df,
        x='Time',
        y='Mass Loss',
        color='Measurement',  # Use 'Measurement' for coloring and labeling the lines
        labels={'Time': 'Time [years]', 'Mass Loss': 'Mass loss [um]'},
        title="Mass Loss Over Time",
        height=700
    )

    fig.update_layout(
        yaxis_type=yaxis_type,
        showlegend=True,  # Ensure the legend is displayed
        legend_title="Measurements"  # Properly label the legend
    )

    return fig


def display_plot_html(fig):
    """Displays the generated Plotly figure as HTML in Streamlit."""
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    components.html(
        f"""
        <div style="background-color: white; padding: 10px; border-radius: 10px;">
            {plot_html}
        </div>
        """,
        height=800,
        scrolling=True
    )


def display_measurement_view(container):
    """
    Displays the measurement view interface for selecting and analyzing corrosion measurements.

    Args:
        container (st.container): The Streamlit container in which the measurement view interface will be displayed.
    """
    measurement_directories = [
        '../data/kadi4mat_json/immersion_corrosion_measurements/',
    ]

    measurements = load_corrosion_measurements_from_directory(measurement_directories, corwiz_measurements)

    global plot_data

    with container:
        st.write("---")
        st.header("Corrosion mass loss measurements")

        main_content = st.container()
        description_content = st.container()

        measurement_process_pairs = get_corrosion_process_type(measurements)

        with main_content:
            plot_column, selection_column = st.columns((1, 1))

            with selection_column:
                corrosion_types = sorted({process_type for _, process_type in measurement_process_pairs})
                selected_corrosion_type = st.selectbox('**Corrosion Type**', corrosion_types)

                filtered_measurements = [measurement for measurement, process_type in measurement_process_pairs if
                                   process_type == selected_corrosion_type]
                selected_measurement = st.selectbox(
                    '**Measurement**', filtered_measurements,
                    format_func=lambda measurement: measurement.name + " (" + measurement.kadi_identifier + ")", key="measurement_selectbox"
                )

                # Display parameters and compute corrosion speed and exponent using the selected time
                selected_measurement.display_parameters()

                # Display the location associated with the measurement on the map 
                if selected_measurement.measurement_coordinates is not None:
                    st.map(selected_measurement.measurement_coordinates)

                # Obtain the plotting data for the selected measurement
                plot_data = selected_measurement.get_material_loss()

            with plot_column:
                pass

        with description_content:
            description_expander = st.expander("**Measurement Description**", expanded=False)

            with description_expander:
                display_measurement_info(selected_measurement)
