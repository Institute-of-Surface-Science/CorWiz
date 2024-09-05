import plotly.express as px
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from typing import List
from models import CorrosionModel

def generate_plot(models: List[CorrosionModel], current_model: CorrosionModel, time_range: float):
    """
    Generates and returns a Plotly Express figure for mass loss over time.

    Args:
        models (List[CorrosionModel]): List of corrosion models to be plotted.
        current_model (CorrosionModel): The currently selected model to plot.
        time_range (float): The time range (years) for which to evaluate material loss.

    Returns:
        plotly.graph_objects.Figure: The generated plot showing mass loss over time.
    """
    t = np.linspace(0, time_range, 400)
    plot_data = []
    all_y_values = []

    # Add current model's data
    current_model_loss = current_model.evaluate_material_loss(t)
    current_model_df = pd.DataFrame({'Time': t, 'Mass Loss': current_model_loss, 'Model': f"{current_model.model_name} (live)"})
    plot_data.append(current_model_df)
    all_y_values.append(current_model_loss)

    # Add additional models' data
    for i, model in enumerate(models, start=1):
        model_loss = model.evaluate_material_loss(t)
        model_df = pd.DataFrame({'Time': t, 'Mass Loss': model_loss, 'Model': f"{model.model_name} ({i})"})
        plot_data.append(model_df)
        all_y_values.append(model_loss)

    # Combine all data for plotting
    plot_df = pd.concat(plot_data)

    # Determine y-axis scale (log or linear) based on the ratio between max and min values
    yaxis_type = "linear"
    positive_y_values = np.concatenate(all_y_values)[np.concatenate(all_y_values) > 0]
    if positive_y_values.size > 0:
        max_value, min_value = np.max(positive_y_values), np.min(positive_y_values)
        if max_value / min_value > 100:
            yaxis_type = "log"

    px.defaults.template = "plotly_white"

    # Generate plot using Plotly Express
    fig = px.line(
        plot_df,
        x='Time',
        y='Mass Loss',
        color='Model',  # Use 'Model' column to color and label the lines
        labels={'Time': 'Time [years]', 'Mass Loss': 'Mass loss [μm]'},
        title="Mass Loss Over Time",
        height=700
    )

    fig.update_layout(
        yaxis_type=yaxis_type,
        showlegend=True,
        legend_title="Models"
    )

    return fig


def display_plot_html(fig):
    """
    Renders the Plotly figure in Streamlit as HTML.

    Args:
        fig (plotly.graph_objects.Figure): The figure to be displayed.
    """
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
