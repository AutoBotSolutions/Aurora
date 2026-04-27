"""
===============================================================================
AI Visual Dashboard
===============================================================================
The AI Visual Dashboard provides a live and interactive interface for monitoring
pipeline performance and model predictions. Built with Dash and Plotly, this tool
is designed to showcase meaningful insights into AI workflows, allowing users to
explore dynamic metrics and make informed decisions based on real-time data.

GitHub Repository: <https://github.com/your-repo> (Replace with your repository link)
License: MIT License (or other preferred open-source license)
Maintainer: G.O.D Framework Team
===============================================================================
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


class AIPipelineDashboard:
    """
    AI Pipeline Dashboard for visualizing metrics and predictions.

    This class provides an interactive web-based dashboard built using the Dash
    framework. The dashboard enables visualization of metrics and scatter plots
    of predictions vs. ground truths. Users can select metrics to explore trends
    and inspect model performance using the UI.

    :ivar metrics_data: Stores the DataFrame containing metrics data, such as accuracy, precision, and loss values.
    :type metrics_data: pd.DataFrame
    :ivar predictions_data: Stores the DataFrame containing predictions and ground truth values.
    :type predictions_data: pd.DataFrame
    :ivar app: Dash app instance used to create and run the dashboard.
    :type app: dash.Dash
    """

    def __init__(self, metrics_data: pd.DataFrame, predictions_data: pd.DataFrame):
        """
        Initialize the dashboard with the required data.

        Args:
            metrics_data (pd.DataFrame): DataFrame containing metrics (e.g., accuracy, precision, loss).
            predictions_data (pd.DataFrame): DataFrame containing predictions and ground truth values.
        """
        self.metrics_data = metrics_data
        self.predictions_data = predictions_data
        self.app = dash.Dash(__name__)

    def build_dashboard(self):
        """
        Build the dashboard layout and define interactivity using Dash callbacks.
        """
        self.app.layout = html.Div([
            html.H1("AI Pipeline Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),

            # Metric Selection Dropdown
            html.Div([
                html.Label("Select Metric:", style={"marginRight": "10px"}),
                dcc.Dropdown(
                    id="metric-selector",
                    options=[{"label": col, "value": col} for col in self.metrics_data.columns],
                    value=self.metrics_data.columns[0],
                    style={"width": "50%"}
                )
            ], style={"textAlign": "center", "marginBottom": "20px"}),

            # Metric Trend Chart
            html.Div([dcc.Graph(id="metric-trend-chart")], style={"marginBottom": "30px"}),

            # Predictions Scatter Plot
            html.Div([dcc.Graph(id="predictions-chart")])
        ])

        # Callback for updating the Metric Trend Chart
        @self.app.callback(
            Output("metric-trend-chart", "figure"),
            Input("metric-selector", "value")
        )
        def update_metric_chart(selected_metric):
            figure = px.line(
                self.metrics_data,
                y=selected_metric,
                title=f"Metric Trend: {selected_metric}",
                labels={"value": "Metric Value", "index": "Index"}
            )
            figure.update_layout(template="plotly_white")
            return figure

        # Callback for updating the Predictions Scatter Plot
        @self.app.callback(
            Output("predictions-chart", "figure"),
            Input("metric-selector", "value")  # Keeping input to enable future feature extensions
        )
        def update_predictions_chart(selected_metric):
            figure = px.scatter(
                self.predictions_data,
                x="predicted",
                y="actual",
                title="Predictions vs Actual",
                labels={
                    "predicted": "Predicted Value",
                    "actual": "Actual Value"
                },
                color_continuous_scale="Viridis"
            )
            figure.update_layout(template="plotly_white")
            return figure

    def run(self, host: str = "0.0.0.0", port: int = 8050, debug: bool = False):
        """
        Launch the Dash web server to render the dashboard.

        Args:
            host (str, optional): Host IP address to bind the server. Defaults to "0.0.0.0".
            port (int, optional): Port number to run the server. Defaults to 8050.
            debug (bool, optional): Debug mode for the web server. Defaults to False.
        """
        self.build_dashboard()
        self.app.run_server(host=host, port=port, debug=debug)


if __name__ == "__main__":
    # Example usage with sample datasets
    metrics_df = pd.DataFrame({
        "epoch": [1, 2, 3, 4, 5],
        "accuracy": [0.78, 0.82, 0.85, 0.88, 0.89],
        "loss": [0.42, 0.36, 0.30, 0.27, 0.23]
    })
    predictions_df = pd.DataFrame({
        "predicted": [0.9, 0.85, 0.8, 0.4, 0.3],
        "actual": [1, 0.9, 0.7, 0.5, 0.2]
    })

    # Initialize and run the dashboard
    dashboard = AIPipelineDashboard(metrics_data=metrics_df, predictions_data=predictions_df)
    dashboard.run(debug=True)