"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score


class CrossValidationAndOptimization:
    """
    Performs cross-validation and hyperparameter optimization for a machine learning model.

    This class is designed to facilitate the evaluation and tuning of machine learning models
    by providing methods for cross-validation and hyperparameter searching. It supports both
    grid search and randomized search for hyperparameter optimization and allows for logging
    of intermediate steps and results.

    :ivar model: The machine learning model used for training and evaluation.
    :type model: Any estimator compatible with scikit-learn
    :ivar param_grid: The hyperparameter grid or parameter distributions for optimization.
    :type param_grid: dict
    :ivar search_type: The search strategy for tuning hyperparameters, either "grid" or "random".
    :type search_type: str
    :ivar scoring: The metric used for evaluating the model's performance.
    :type scoring: str
    :ivar logger: A logger instance for logging messages.
    :type logger: logging.Logger
    """

    def __init__(self, model, param_grid, search_type="grid", scoring="accuracy"):
        """
        Initialize the class with a machine learning model and hyperparameter grid.

        :param model: The machine learning model (e.g., RandomForestClassifier).
        :param param_grid: A dictionary of hyperparameter ranges for tuning.
        :param search_type: Type of hyperparameter search, "grid" (default) or "random".
        :param scoring: Metric for evaluating model performance (default: "accuracy").
        """
        self.model = model
        self.param_grid = param_grid
        self.search_type = search_type
        self.scoring = scoring
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configures and returns a logger instance.

        :return: Configured logger instance.
        """
        logger = logging.getLogger("CrossValidationAndOptimization")
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def cross_validate(self, X, y, cv=5):
        """
        Perform k-fold cross-validation on the model and log results.

        :param X: Input features (features matrix).
        :param y: Target labels (label vector).
        :param cv: Number of cross-validation splits (default: 5).
        :return: Cross-validation scores as a list.
        """
        self.logger.info("Starting cross-validation...")
        try:
            scores = cross_val_score(self.model, X, y, cv=cv, scoring=self.scoring)
            self.logger.info(f"Cross-validation scores: {scores}")
            self.logger.info(f"Mean score: {scores.mean():.4f}")
            return scores
        except Exception as e:
            self.logger.error(f"Error during cross-validation: {e}")
            raise

    def optimize_hyperparameters(self, X, y, cv=5, n_iter=10):
        """
        Perform hyperparameter optimization using GridSearchCV or RandomizedSearchCV.

        :param X: Input features (features matrix).
        :param y: Target labels (label vector).
        :param cv: Number of cross-validation splits (default: 5).
        :param n_iter: Number of iterations for RandomizedSearchCV (default: 10, ignored for GridSearchCV).
        :return: Best parameters and the trained model.
        """
        self.logger.info(f"Starting hyperparameter search using {self.search_type} search...")

        try:
            if self.search_type == "grid":
                search = GridSearchCV(
                    estimator=self.model, param_grid=self.param_grid, cv=cv, scoring=self.scoring
                )
            elif self.search_type == "random":
                search = RandomizedSearchCV(
                    estimator=self.model,
                    param_distributions=self.param_grid,
                    cv=cv,
                    scoring=self.scoring,
                    n_iter=n_iter,
                    random_state=42,
                )
            else:
                raise ValueError(f"Invalid search type: {self.search_type}. Use 'grid' or 'random'.")

            search.fit(X, y)
            self.logger.info(f"Best parameters found: {search.best_params_}")
            self.logger.info(f"Best cross-validation score: {search.best_score_:.4f}")
            return search.best_params_, search.best_estimator_

        except Exception as e:
            self.logger.error(f"Error during hyperparameter optimization: {e}")
            raise


if __name__ == "__main__":
    # Example usage
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification

    # Generate sample data
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_classes=2,
        class_sep=2,
        random_state=42,
        weights=[0.1, 0.9],
    )

    # Define the model
    model = RandomForestClassifier(random_state=42)

    # Define hyperparameter grid
    param_grid = {
        "n_estimators": [50, 100, 150],
        "max_depth": [5, 10, 15],
        "min_samples_split": [2, 5, 10],
    }

    # Instantiate the optimizer class
    optimizer = CrossValidationAndOptimization(model=model, param_grid=param_grid, search_type="grid")

    # Perform cross-validation
    print("\nPerforming Cross-Validation:")
    cv_scores = optimizer.cross_validate(X, y, cv=5)

    # Perform hyperparameter optimization
    print("\nPerforming Hyperparameter Optimization:")
    best_params, best_model = optimizer.optimize_hyperparameters(X, y, cv=5)

    # Display results
    print("\nResults:")
    print(f"Best Parameters: {best_params}")
    print(f"Best Cross-Validation Score: {cv_scores.mean():.4f}")
