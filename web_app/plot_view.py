import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit.components.v1 as components
from typing import List, Optional, Dict
from models import CorrosionModel

def generate_plot(
    models: List[CorrosionModel],
    current_model: CorrosionModel,
    time_range: float,
    measurements: Optional[List[dict]] = None,
    resolution: Optional[int] = 400,
    height: Optional[int] = 700,
    width: Optional[int] = None
):
    """
    Generates and returns a Plotly figure with subplots for different y-axis labels (units) for mass loss over time.
    Models are plotted as line plots, and measurements are plotted as scatter points.

    Args:
        models (List[CorrosionModel]): List of corrosion models to be plotted.
        current_model (CorrosionModel): The currently selected model to plot.
        time_range (float): The time range (years) for which to evaluate material loss.
        measurements (Optional[List[dict]]): Optional list of measurements, where each item is a dict with keys:
                                             'name' (str) for the measurement name, and 'data' (np.ndarray) for the data matrix.
                                             Each matrix is expected to have two columns: time and mass loss.
        resolution (Optional[int]): The number of points used to plot the curve. Higher values give smoother plots. Defaults to 400.
        height (Optional[int]): Custom height of the plot. Defaults to 700.
        width (Optional[int]): Custom width of the plot. Defaults to None (auto).

    Returns:
        plotly.graph_objects.Figure: The generated plot with multiple subplots when axis labels differ.
    """
    t = np.linspace(0, time_range, resolution)

    # Dictionary to store the data based on unique axis labels
    axis_mapping: Dict[str, Dict[str, list]] = {}

    def add_to_axis_mapping(x_data, y_data, x_label, y_label, label, plot_type='lines'):
        """Helper function to store traces (lines or markers) in axis mapping based on axis labels."""
        key = f"{x_label}_{y_label}"
        if key not in axis_mapping:
            axis_mapping[key] = {
                "x_label": x_label,
                "y_label": y_label,
                "traces": []
            }
        mode = 'lines' if plot_type == 'lines' else 'markers'
        axis_mapping[key]["traces"].append(go.Scatter(x=x_data, y=y_data, mode=mode, name=label))

    # Evaluate the current model and get its data and axis labels
    current_model_loss, x_axis_label, y_axis_label = current_model.evaluate_material_loss(t)

    # Add the current model to the axis mapping
    add_to_axis_mapping(t, current_model_loss, x_axis_label, y_axis_label, f"{current_model.model_name} (live)")

    # Add additional models to the axis mapping
    for i, model in enumerate(models, start=1):
        model_loss, model_x_axis_label, model_y_axis_label = model.evaluate_material_loss(t)
        add_to_axis_mapping(t, model_loss, model_x_axis_label, model_y_axis_label, f"{model.model_name} ({i})")

    # Add measurements to the axis mapping
    if measurements:
        for measurement in measurements:
            measurement_name = measurement['name']
            measurement_data = measurement['data']
            measurement_x_axis_label = measurement.get('x_axis_label', 'Time [years]')
            measurement_y_axis_label = measurement.get('y_axis_label', 'Mass loss [mg]')
            add_to_axis_mapping(measurement_data[:, 0], measurement_data[:, 1], measurement_x_axis_label,
                                measurement_y_axis_label, measurement_name, plot_type='markers')

    # Create subplots based on the number of unique axis pairs
    num_subplots = len(axis_mapping)
    fig = make_subplots(
        rows=1, cols=num_subplots,  # One row, multiple columns
        shared_xaxes=True,  # Share x-axis between subplots
        horizontal_spacing=0.1,  # Adjust horizontal spacing between subplots
        subplot_titles=[f"{value['x_label']} vs {value['y_label']}" for key, value in axis_mapping.items()]
    )

    # Add the traces to the corresponding subplot
    for idx, (key, axis_data) in enumerate(axis_mapping.items(), start=1):
        for trace in axis_data['traces']:
            fig.add_trace(trace, row=1, col=idx)
        # Set the y-axis title for this subplot
        fig.update_yaxes(title_text=axis_data['y_label'], row=1, col=idx)

    # Set the common x-axis title
    fig.update_xaxes(title_text=x_axis_label, row=1, col=1)

    # Update the layout for the entire figure
    fig.update_layout(
        height=height,
        width=width,
        title="Mass Loss Over Time {CorWiz}",
        showlegend=True,  # Ensure the legend is shown
        template="plotly_white",
        legend_title="Models and Measurements"
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
