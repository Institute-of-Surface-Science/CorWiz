import plotly.express as px
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from typing import List, Optional
from models import CorrosionModel

def generate_plot(
    models: List[CorrosionModel],
    current_model: CorrosionModel,
    time_range: float,
    x_axis_label: Optional[str] = 'Time [years]',
    y_axis_label: Optional[str] = 'Mass loss [μm]',
    resolution: Optional[int] = 400,
    height: Optional[int] = 700,
    width: Optional[int] = None
):
    """
    Generates and returns a Plotly Express figure for mass loss over time, with optional axis labels, resolution, and dimensions.

    Args:
        models (List[CorrosionModel]): List of corrosion models to be plotted.
        current_model (CorrosionModel): The currently selected model to plot.
        time_range (float): The time range (years) for which to evaluate material loss.
        x_axis_label (Optional[str]): Custom label for the x-axis. Defaults to 'Time [years]'.
        y_axis_label (Optional[str]): Custom label for the y-axis. Defaults to 'Mass loss [μm]'.
        resolution (Optional[int]): The number of points used to plot the curve. Higher values give smoother plots. Defaults to 400.
        height (Optional[int]): Custom height of the plot. Defaults to 700.
        width (Optional[int]): Custom width of the plot. Defaults to None (auto).

    Returns:
        plotly.graph_objects.Figure: The generated plot showing mass loss over time.
    """
    t = np.linspace(0, time_range, resolution)

    # Initialize a list for plotting
    plot_data = []

    # Plot the current model's data first
    current_model_loss = current_model.evaluate_material_loss(t)
    current_model_df = pd.DataFrame(
        {'Time': t, 'Mass Loss': current_model_loss, 'Model': f"{current_model.model_name} (live)"})
    plot_data.append(current_model_df)

    # Collect all y-values to check for max/min difference for log scaling
    all_y_values = [current_model_loss]

    # Plot the additional models
    for i, model in enumerate(models, start=1):
        model_loss = model.evaluate_material_loss(t)
        model_df = pd.DataFrame({'Time': t, 'Mass Loss': model_loss, 'Model': f"{model.model_name} ({i})"})
        plot_data.append(model_df)
        all_y_values.append(model_loss)

    # Combine all data into a single DataFrame
    plot_df = pd.concat(plot_data)

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

    # Plot using Plotly Express and use 'Model' for distinct colors and labels
    fig = px.line(
        plot_df,
        x='Time',
        y='Mass Loss',
        color='Model',  # Use 'Model' for coloring and labeling the lines
        labels={'Time': x_axis_label, 'Mass Loss': y_axis_label},
        title="Mass Loss Over Time",
        height=height,
        width=width  # Allow width to be set dynamically
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