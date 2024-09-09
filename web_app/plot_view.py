import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from typing import List, Optional
from models import CorrosionModel

def generate_plot(
    models: List[CorrosionModel],
    current_model: CorrosionModel,
    time_range: float,
    measurements: Optional[List[dict]] = None,  # Add measurements as an optional parameter
    x_axis_label: Optional[str] = 'Time [years]',
    y_axis_label: Optional[str] = 'Mass loss [μm]',
    resolution: Optional[int] = 400,
    height: Optional[int] = 700,
    width: Optional[int] = None
):
    """
    Generates and returns a Plotly figure for mass loss over time, with optional axis labels, resolution, and dimensions.
    Models are plotted as line plots, and measurements are plotted as scatter points.

    Args:
        models (List[CorrosionModel]): List of corrosion models to be plotted.
        current_model (CorrosionModel): The currently selected model to plot.
        time_range (float): The time range (years) for which to evaluate material loss.
        measurements (Optional[List[dict]]): Optional list of measurements, where each item is a dict with keys:
                                             'name' (str) for the measurement name, and 'data' (np.ndarray) for the data matrix.
                                             Each matrix is expected to have two columns: time and mass loss.
        x_axis_label (Optional[str]): Custom label for the x-axis. Defaults to 'Time [years]'.
        y_axis_label (Optional[str]): Custom label for the y-axis. Defaults to 'Mass loss [μm]'.
        resolution (Optional[int]): The number of points used to plot the curve. Higher values give smoother plots. Defaults to 400.
        height (Optional[int]): Custom height of the plot. Defaults to 700.
        width (Optional[int]): Custom width of the plot. Defaults to None (auto).

    Returns:
        plotly.graph_objects.Figure: The generated plot showing mass loss over time.
    """
    t = np.linspace(0, time_range, resolution)

    # Initialize the plotly figure with lines for the models
    fig = go.Figure()

    # Plot the current model's data as a line
    current_model_loss = current_model.evaluate_material_loss(t)
    fig.add_trace(go.Scatter(x=t, y=current_model_loss, mode='lines', name=f"{current_model.model_name} (live)"))

    # Collect all y-values to check for max/min difference for log scaling
    all_y_values = [current_model_loss]

    # Plot the additional models as lines
    for i, model in enumerate(models, start=1):
        model_loss = model.evaluate_material_loss(t)
        fig.add_trace(go.Scatter(x=t, y=model_loss, mode='lines', name=f"{model.model_name} ({i})"))
        all_y_values.append(model_loss)

    # If measurements are provided, plot them as scatter points
    if measurements:
        for measurement in measurements:
            measurement_name = measurement['name']
            measurement_data = measurement['data']  # Expecting a 2D array with time and mass loss
            fig.add_trace(go.Scatter(
                x=measurement_data[:, 0],
                y=measurement_data[:, 1],
                mode='markers',
                name=measurement_name,  # Use the measurement name as the label
                marker=dict(symbol='circle', size=8)
            ))
            all_y_values.append(measurement_data[:, 1])

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

    # Update layout for the figure
    fig.update_layout(
        yaxis_type=yaxis_type,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        title="Mass Loss Over Time",
        height=height,
        width=width,
        showlegend=True,
        legend_title="Models and Measurements",
        template="plotly_white"
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
