"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
Visualization Module
====================

An easy-to-use and highly customizable visualization utility designed for the G.O.D Framework, 
supporting static plots and interactive analytics for machine learning workflows. This module provides 
a powerful set of tools to render insightful visualizations for training, evaluation, and other analytics 
purposes.

Features:
    - Plotting training and evaluation metrics.
    - Customization options for themes, titles, and file exporting.
    - Interactive visualizations via Plotly.
    - Seamless integration into ML/DL pipelines for better interpretability.

GitHub Repository: <Insert Repository URL>
License: MIT License
Maintainer: G.O.D Framework Team
"""

import logging
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd


class Visualization:
    """
    Provides tools for data visualization, including traditional plotting with Matplotlib
    and Seaborn, as well as interactive graph generation using Plotly.

    The Visualization class encapsulates methods for generating and customizing plots,
    such as time series plots, metric visualizations, and interactive visualizations.
    It also supports theme customization for consistent styling and exporting plots
    as files for sharing or analysis.

    :ivar theme: Current visualization theme used by Seaborn.
    :type theme: str
    """

    def __init__(self):
        """
        Initializes the Visualization class with a default theme for plots.
        """
        self.theme = "default"
        sns.set_theme(style=self.theme)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def set_theme(self, theme_name="default"):
        """
        Sets the theme for plots (using Seaborn).
        
        Args:
            theme_name (str): Name of the theme. Options include "default", "darkgrid", "lightgrid", and more.
        """
        self.theme = theme_name
        sns.set_theme(style=theme_name)
        logging.info(f"Theme set to: {theme_name}")

    @staticmethod
    def plot_metrics(metrics, title="Training Metrics", xlabel="Epochs", ylabel="Values", save_path=None):
        """
        Plots training or evaluation metrics using Matplotlib.
        
        Args:
            metrics (dict): Dictionary of metric values where keys are metric names 
                            (e.g., 'accuracy', 'loss') and values are lists of numbers.
            title (str): Title of the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            save_path (str): File path to save the plot as an image. Optional.
        """
        logging.info("Initializing metric plotting...")
        try:
            plt.figure(figsize=(10, 6))
            for key, values in metrics.items():
                plt.plot(values, label=key, marker='o')
            plt.legend()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            if save_path:
                plt.savefig(save_path, dpi=300)
                logging.info(f"Metrics plot saved to {save_path}")
            plt.show()
            logging.info("Metrics plotted successfully.")
        except Exception as e:
            logging.error(f"Error while plotting metrics: {e}")

    def plot_time_series(self, data, x, y, title="Time Series Plot", save_path=None):
        """
        Creates a time series plot from a pandas DataFrame.
        
        Args:
            data (pd.DataFrame): Data for plotting, typically with a datetime index.
            x (str): Name of the column for the x-axis.
            y (str): Name of the column for the y-axis.
            title (str): Title of the time series plot.
            save_path (str): File path to save the plot as an image (optional).
        """
        logging.info("Creating time series plot...")
        try:
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=data, x=x, y=y)
            plt.title(title)
            plt.xlabel(x)
            plt.ylabel(y)
            if save_path:
                plt.savefig(save_path, dpi=300)
                logging.info(f"Time series plot saved to {save_path}")
            plt.show()
            logging.info("Time series plotted successfully.")
        except Exception as e:
            logging.error(f"Error while plotting time series: {e}")

    @staticmethod
    def create_interactive_plot(data, x, y, color=None, plot_type="scatter"):
        """
        Creates an interactive plot using Plotly.
        
        Args:
            data (pd.DataFrame): Data for the plot.
            x (str): Column name for x-axis values.
            y (str): Column name for y-axis values.
            color (str): Column name for color encoding (optional).
            plot_type (str): Type of interactive plot ("scatter" or "line").
        
        Returns:
            plotly.graph_objs._figure.Figure: Interactive plot as a Plotly figure object.
        """
        logging.info("Creating interactive plot...")
        try:
            if plot_type == "scatter":
                fig = px.scatter(data, x=x, y=y, color=color, title="Interactive Scatter Plot")
            elif plot_type == "line":
                fig = px.line(data, x=x, y=y, color=color, title="Interactive Line Plot")
            else:
                raise ValueError("Unsupported plot type. Options are: 'scatter' or 'line'.")
            fig.show()
            logging.info("Interactive plot created successfully.")
            return fig
        except Exception as e:
            logging.error(f"Error while creating interactive plot: {e}")

    @staticmethod
    def export_to_file(fig, filepath):
        """
        Exports a Plotly interactive plot to a file.
        
        Args:
            fig (plotly.graph_objs._figure.Figure): Plotly figure to export.
            filepath (str): Destination file path (e.g., './output/plot.html').
        """
        logging.info(f"Exporting interactive plot to {filepath}...")
        try:
            fig.write_html(filepath)
            logging.info(f"Plot exported successfully to {filepath}.")
        except Exception as e:
            logging.error(f"Error while exporting plot: {e}")


# Example Usage (comment/remove before open-source submission)
if __name__ == "__main__":
    # Example data
    metrics = {
        "accuracy": [0.7, 0.8, 0.85, 0.9],
        "loss": [0.6, 0.4, 0.3, 0.2]
    }
    df = pd.DataFrame({
        "time": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "value": [100, 200, 150, 300]
    })

    # Visualization instance
    visualizer = Visualization()

    # Plot metrics
    visualizer.plot_metrics(metrics, save_path="metrics_plot.png")

    # Plot time series
    visualizer.plot_time_series(df, x="time", y="value", title="Sample Time Series")

    # Interactive example
    interactive_fig = visualizer.create_interactive_plot(df, x="time", y="value", plot_type="line")
    visualizer.export_to_file(interactive_fig, "interactive_plot.html")
