"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import pandas as pd
from typing import List, Dict


class BiasAuditor:
    """
    Facilitates fairness analysis and bias detection in datasets based on
    specified protected features and an outcome feature.

    This class provides methods to evaluate bias across groups defined by
    protected features and visualize the results. It uses fairness gap
    thresholds to flag biased outcomes and provide insights into disparities
    in datasets.

    :ivar protected_features: List of features used for bias evaluation.
                              These features denote sensitive or protected groups.
    :type protected_features: List[str]
    :ivar outcome_feature: Represents the feature or metric measuring outcomes
                           (e.g., accuracy, prediction performance).
    :type outcome_feature: str
    :ivar bias_threshold: Threshold value to identify fairness gaps.
                          Fairness gaps exceeding this value indicate bias.
                          The default is 0.1.
    :type bias_threshold: float
    """

    def __init__(self, protected_features: List[str], outcome_feature: str, bias_threshold: float = 0.1):
        """
        Initializes the BiasAuditor for fairness analysis.

        :param protected_features: List of features to audit for bias (e.g., ["gender", "race"]).
        :param outcome_feature: Feature or metric measuring outcomes (e.g., prediction_accuracy).
        :param bias_threshold: Threshold for fairness gaps indicating bias (default is 0.1).
        """
        self.protected_features = protected_features
        self.outcome_feature = outcome_feature
        self.bias_threshold = bias_threshold

    def evaluate_bias(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """
        Evaluates bias in the dataset for each protected feature.

        :param data: Pandas DataFrame containing the dataset for analysis.
                     It must include the protected features and the outcome feature.
        :return: A dictionary summarizing bias analysis for each protected feature.
        """
        report = {}

        for feature in self.protected_features:
            if feature not in data.columns:
                raise ValueError(f"Protected feature '{feature}' is missing from the dataset.")
            if self.outcome_feature not in data.columns:
                raise ValueError(f"Outcome feature '{self.outcome_feature}' is missing from the dataset.")

            # Group statistics by protected feature
            group_stats = data.groupby(feature)[self.outcome_feature].mean()
            fairness_gap = group_stats.max() - group_stats.min()

            # Append results to bias report
            report[feature] = {
                "group_stats": group_stats.to_dict(),
                "fairness_gap": fairness_gap,
                "is_biased": fairness_gap > self.bias_threshold  # Flag as biased if fairness gap exceeds threshold
            }

        return report

    def visualize_bias(self, data: pd.DataFrame, feature: str):
        """
        Generates a heatmap visualization for group-wise fairness analysis.

        :param data: Pandas DataFrame containing the dataset.
        :param feature: Protected feature for which to visualize the bias.
        """
        import seaborn as sns
        import matplotlib.pyplot as plt

        if feature not in data.columns:
            raise ValueError(f"Protected feature '{feature}' is missing from the dataset.")
        if self.outcome_feature not in data.columns:
            raise ValueError(f"Outcome feature '{self.outcome_feature}' is missing from the dataset.")

        # Generate a heatmap for group distribution
        heatmap_data = pd.crosstab(
            data[feature], data[self.outcome_feature], normalize="index"
        )
        sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"Bias Heatmap for {feature}")
        plt.xlabel(self.outcome_feature)
        plt.ylabel(feature)
        plt.show()


if __name__ == "__main__":
    # Example dataset
    sample_data = pd.DataFrame({
        "gender": ["male", "female", "male", "female", "male", "female"],
        "race": ["white", "black", "black", "white", "asian", "asian"],
        "prediction_accuracy": [0.9, 0.7, 0.8, 0.85, 0.92, 0.9]
    })

    # Initialize the BiasAuditor
    print("Initializing Bias Auditor...")
    auditor = BiasAuditor(protected_features=["gender", "race"], outcome_feature="prediction_accuracy")

    # Evaluate bias in the dataset
    print("Evaluating Bias...")
    bias_report = auditor.evaluate_bias(sample_data)
    print("\nBias Analysis Report:")
    for feature, details in bias_report.items():
        print(f"{feature}:")
        print(f"  Group Stats: {details['group_stats']}")
        print(f"  Fairness Gap: {details['fairness_gap']:.2f}")
        print(f"  Is Biased: {details['is_biased']}")

    # Visualize bias for a specific feature
    print("\nVisualizing Bias for 'gender'...")
    auditor.visualize_bias(sample_data, feature="gender")
