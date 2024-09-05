import plotly.express as px
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

def generate_plot(models, current_model, time_range):
    """Generates and returns a Plotly Express figure for mass loss over time."""
    t = np.linspace(0, time_range, 400)

    # Initialize a list for plotting
    plot_df = []

    # Plot the current model's data first
    D = current_model.evaluate_material_loss(t)
    current_model_data = pd.DataFrame(
        {'Time': t, 'Mass Loss': D, 'Model': f"{current_model.model_name} (live)"})
    plot_df.append(current_model_data)

    # Collect all y-values to check for max/min difference for log scaling
    all_y_values = [D]

    # Plot the additional models
    model_counter = 1
    for model in models:
        D = model.evaluate_material_loss(t)
        model_data = pd.DataFrame({'Time': t, 'Mass Loss': D, 'Model': f"{model.model_name} ({model_counter})"})
        plot_df.append(model_data)
        all_y_values.append(D)
        model_counter += 1

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

    # Plot using Plotly Express and use 'Model' for distinct colors and labels
    fig = px.line(
        plot_df,
        x='Time',
        y='Mass Loss',
        color='Model',  # Use 'Model' for coloring and labeling the lines
        labels={'Time': 'Time [years]', 'Mass Loss': 'Mass loss [um]'},
        title="Mass Loss Over Time",
        height=700
    )

    fig.update_layout(
        yaxis_type=yaxis_type,
        showlegend=True,  # Ensure the legend is displayed
        legend_title="Models"  # Properly label the legend
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
