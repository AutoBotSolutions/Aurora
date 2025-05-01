"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Pipeline Optimizer

The AI Pipeline Optimizer is designed to automate the optimization of machine learning models through hyperparameter tuning.
By leveraging scikit-learn's GridSearchCV and other compatible frameworks, it improves predictive performance and streamlines
the pipeline tuning process for developers and data scientists.

---

Core Features:
1. Automatic hyperparameter tuning using grid search.
2. Integration with scikit-learn pipelines as well as custom models via a standardized interface.
3. Support for customizable scoring metrics and cross-validation strategies.
4. Modular and extensible design for easy integration into larger workflows.

---

Usage:
    python ai_pipeline_optimizer.py

Examples:
    from sklearn.ensemble import RandomForestClassifier
    from ai_pipeline_optimizer import PipelineOptimizer

    param_grid = {
        "n_estimators": [10, 50, 100],
        "max_depth": [None, 10, 20],
    }

    optimizer = PipelineOptimizer(
        model=RandomForestClassifier(),
        param_grid=param_grid
    )
    optimized_model = optimizer.optimize(X_train, y_train)

Dependencies:
    - scikit-learn>=0.24.0 : Required for GridSearchCV and machine learning functionality.
    Install with: pip install scikit-learn
"""

from sklearn.model_selection import GridSearchCV
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class PipelineOptimizer:
    """
    Facilitates the optimization of machine learning model hyperparameters using grid search.

    This class wraps scikit-learn's GridSearchCV to provide a simpler interface for
    hyperparameter optimization, using a predefined grid of parameters. It is designed to
    search the parameter space systematically and return the best possible configuration
    based on the provided scoring metric.

    :ivar model: The machine learning model to optimize, compatible with scikit-learn.
    :type model: object
    :ivar param_grid: Dictionary specifying the grid of hyperparameters to search through.
    :type param_grid: dict
    :ivar cv: Number of cross-validation folds to use during grid search.
    :type cv: int
    :ivar scoring: The scoring metric to evaluate model performance.
    :type scoring: str
    :ivar verbose: Level of verbosity for the search process.
    :type verbose: int
    """

    def __init__(self, model, param_grid, cv=5, scoring="accuracy", verbose=1):
        """
        Initializes the PipelineOptimizer class.

        :param model: A scikit-learn compatible model instance (e.g., RandomForestClassifier).
        :param param_grid: Dictionary of hyperparameter options to search across.
        :param cv: Number of cross-validation folds to use (default: 5).
        :param scoring: Scoring metric used for evaluating models (default: "accuracy").
        :param verbose: Verbose level for GridSearchCV (default: 1).
        """
        self.model = model
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.verbose = verbose

        logger.info("PipelineOptimizer initialized with model: %s", model.__class__.__name__)

    def optimize(self, X_train, y_train):
        """
        Conducts a grid search to find the best hyperparameter configuration for the model.

        :param X_train: The training feature set.
        :param y_train: The training target labels.
        :return: Trained model with the best hyperparameter configuration.
        """
        logger.info("Starting optimization with GridSearchCV...")
        try:
            grid_search = GridSearchCV(
                estimator=self.model,
                param_grid=self.param_grid,
                cv=self.cv,
                scoring=self.scoring,
                verbose=self.verbose
            )
            grid_search.fit(X_train, y_train)
            best_params = grid_search.best_params_
            logger.info("Optimization complete! Best parameters: %s", best_params)
            return grid_search.best_estimator_
        except Exception as e:
            logger.error("Error during optimization: %s", str(e))
            raise e


# Usage example for 'if __name__ == "__main__"' (Modifiable/Optional)
if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split

    # Generate synthetic dataset for demonstration
    logger.info("Generating synthetic dataset for demonstration...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_classes=2,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define model and parameter grid
    param_grid = {
        "n_estimators": [10, 50, 100],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
    }

    # Initialize the optimizer
    optimizer = PipelineOptimizer(
        model=RandomForestClassifier(),
        param_grid=param_grid
    )

    # Optimize hyperparameters
    logger.info("Running hyperparameter optimization...")
    best_model = optimizer.optimize(X_train, y_train)

    # Evaluate the optimized model
    accuracy = best_model.score(X_test, y_test)
    logger.info("Optimized Model Test Accuracy: %.2f%%", accuracy * 100)
