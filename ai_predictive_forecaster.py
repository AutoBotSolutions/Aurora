"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
ai_predictive_forecaster.py

A modular and scalable Python script for time-series forecasting using the ARIMA model. 
Developed as part of the G.O.D. Framework, this utility is designed to provide accurate 
predictions for historical datasets with methods for easy integration and extensibility.

Licensed under MIT License
"""

from statsmodels.tsa.arima.model import ARIMA


class PredictiveForecaster:
    """
    Handles the creation, fitting, and forecasting of time-series models
    using ARIMA. The class is designed to streamline time-series analysis
    by providing a simplified interface for model configuration, fitting
    the historical data, and generating future predictions.

    :ivar model_order: The configuration tuple (`p`, `d`, `q`) for the ARIMA
        model, where `p` is the number of lag observations included, `d` is
        the degree of differencing, and `q` is the moving average order.
    :type model_order: tuple
    :ivar model: The underlying ARIMA model instance fitted to the data.
    :type model: ARIMA or None
    """

    def __init__(self, model_order=(5, 1, 0)):
        """
        Initializes the Predictive Forecaster.

        Args:
            model_order (tuple): Parameters for the ARIMA model (`p`, `d`, `q`).
        """
        self.model_order = model_order
        self.model = None

    def fit(self, data):
        """
        Fits the forecasting model to historical data.

        Args:
            data (list or pandas.Series): The historical time-series data.

        Raises:
            ValueError: If data is empty or invalid.
        """
        if not data or len(data) < 2:
            raise ValueError("Data must contain at least two values to fit a model.")
        try:
            self.model = ARIMA(data, order=self.model_order).fit()
        except Exception as e:
            raise RuntimeError(f"Model fitting failed: {e}")

    def forecast(self, steps=5):
        """
        Generates forecasts for the specified number of steps into the future.

        Args:
            steps (int): Number of future time points to predict.

        Returns:
            list: Predicted values for the future.

        Raises:
            ValueError: If the model is not fitted before calling forecast.
        """
        if self.model is None:
            raise ValueError("Model not fitted yet. Call fit() before making forecasts.")
        try:
            return self.model.forecast(steps=steps).tolist()
        except Exception as e:
            raise RuntimeError(f"Forecasting failed: {e}")


def main():
    """
    The main function demonstrates the process of forecasting using a predictive forecaster.
    It initializes a PredictiveForecaster with a default ARIMA model order, fits it with the
    provided historical data, and performs forecasts for a specified number of future steps.
    The function includes error handling during the fitting and forecasting processes.

    :return: None
    """
    # Example historical time-series data
    historical_data = [100, 110, 125, 130, 120, 150]

    # Initialize the PredictiveForecaster with default ARIMA model order
    forecaster = PredictiveForecaster()

    # Fit the model to the historical data
    try:
        forecaster.fit(historical_data)
    except ValueError as ve:
        print("Error during fitting:", ve)
        return
    except RuntimeError as re:
        print("Unexpected error during fitting:", re)
        return

    # Generate future predictions
    try:
        steps_to_forecast = 3  # Predict the next 3 data points
        future_predictions = forecaster.forecast(steps=steps_to_forecast)
        print("Future Predictions:", future_predictions)
    except ValueError as ve:
        print("Error during forecasting:", ve)
    except RuntimeError as re:
        print("Unexpected error during forecasting:", re)


if __name__ == "__main__":
    main()
