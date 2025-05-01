"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import shap
import matplotlib.pyplot as plt
import pandas as pd
import json


class ExplainabilityManager:
    """
    Manage explainability workflows for machine learning predictions and provide tools for
    analyzing model decisions using SHAP. This class is designed to assist in generating
    interpretable model outputs, batch analysis, exporting explanations, and creating global
    summaries for a dataset.

    :ivar model: Trained machine learning model used for generating SHAP explanations.
    :type model: Any
    :ivar data_sample: Representative sample of the training dataset used as background for SHAP.
    :type data_sample: Any
    :ivar explainer: SHAP explainer instance initialized with the provided model.
    :type explainer: shap.TreeExplainer
    """

    def __init__(self, model, data_sample):
        """
        Initialize the ExplainabilityManager with a trained model and a representative data sample.
        :param model: Trained machine learning model
        :param data_sample: A sample of the training dataset for background distribution (e.g., SHAP expects this)
        """
        self.model = model
        self.data_sample = data_sample
        self.explainer = shap.TreeExplainer(self.model)

    def explain_prediction(self, input_data):
        """
        Explain a single prediction using SHAP values and generate a summary plot.
        :param input_data: Data point for explanation (single row or instance)
        """
        print("Generating SHAP explanation for the provided input...")
        shap_values = self.explainer.shap_values(input_data)

        # Generate SHAP summary plot
        print("Displaying SHAP summary plot...")
        shap.summary_plot(shap_values, input_data, show=True)

    def explain_batch(self, batch_data):
        """
        Explain multiple predictions using SHAP values and generate aggregated summary plots.
        :param batch_data: A batch (subset) of the dataset for explanation (e.g., multiple rows)
        :return: SHAP values array for further analysis
        """
        print("Generating SHAP explanations for the provided batch...")
        shap_values = self.explainer.shap_values(batch_data)

        # Generate summary plot for the batch
        print("Displaying SHAP summary plot for the batch...")
        shap.summary_plot(shap_values, batch_data, show=True)

        return shap_values

    def export_explanations(self, explanations, feature_data, output_format='json', output_path='explanations.json'):
        """
        Export explanations to a specified format (e.g., JSON, HTML).
        :param explanations: SHAP values array
        :param feature_data: Dataset or features corresponding to the SHAP values
        :param output_format: Format of the output file ('json', 'html', or 'csv')
        :param output_path: Path to save the output file
        """
        print(f"Exporting explanations to {output_format.upper()} format...")

        if output_format == 'json':
            # Convert SHAP values to JSON format
            explanation_output = [
                {feature: value for feature, value in zip(feature_data.columns, shap_row)}
                for shap_row in explanations
            ]
            with open(output_path, 'w') as json_file:
                json.dump(explanation_output, json_file, indent=4)
            print(f"Explanations exported as JSON to {output_path}.")

        elif output_format == 'csv':
            # Convert SHAP values to CSV format
            explanation_df = pd.DataFrame(explanations, columns=feature_data.columns)
            explanation_df.to_csv(output_path, index=False)
            print(f"Explanations exported as CSV to {output_path}.")

        elif output_format == 'html':
            # Save SHAP summary plot as an HTML file (requires Matplotlib figure save)
            shap.summary_plot(explanations, feature_data, show=False)
            plt.savefig(output_path, format='html')
            print(f"SHAP summary plot exported as HTML to {output_path}.")

        else:
            raise ValueError(f"Unsupported output format: {output_format}. Use 'json', 'csv', or 'html'.")

    def global_summary(self):
        """
        Generate a global feature importance explanation for the full dataset sample.
        """
        print("Generating global SHAP summary plot for all features...")
        shap_values = self.explainer.shap_values(self.data_sample)

        # Generate global summary plot
        shap.summary_plot(shap_values, self.data_sample, show=True)


# Example Usage
if __name__ == "__main__":
    # Mock Example (Replace these placeholders with real ML model and data)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris

    # Load sample dataset and train model
    iris_data = load_iris()
    X = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    y = iris_data.target

    model = RandomForestClassifier()
    model.fit(X, y)

    # Initialize ExplainabilityManager with model and sample data
    explainability_manager = ExplainabilityManager(model=model, data_sample=X)

    # Generate explanation for a single input
    single_input = X.iloc[0:1]
    explainability_manager.explain_prediction(single_input)

    # Explain a batch of data
    batch_inputs = X.iloc[0:10]
    shap_values_batch = explainability_manager.explain_batch(batch_inputs)

    # Export explanations to a JSON file
    explainability_manager.export_explanations(
        explanations=shap_values_batch,
        feature_data=batch_inputs,
        output_format='json',
        output_path='batch_explanations.json'
    )

    # Generate global summary
    explainability_manager.global_summary()
