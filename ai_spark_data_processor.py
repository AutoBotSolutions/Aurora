"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
===================================================================================
AI Spark Data Processor
===================================================================================

The AI Spark Data Processor is a lightweight framework for distributed data processing
and transformation using Apache Spark. It provides utilities for initializing Spark sessions,
managing data pipelines, and processing large-scale datasets efficiently.

Highlights:
  * Distributed data processing at scale using Spark's parallelism.
  * Flexible dataset loading, transformation, and storage tools.
  * Integration-ready for AI pipelines, training workflows, and batch/real-time processing.

Project Homepage: <https://github.com/<your-repo-link>> (Replace with your GitHub repo)
License: MIT (or preferred open-source license)
Maintainer: G.O.D Framework Team
===================================================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


class SparkDataProcessor:
    """
    A class for processing and transforming data using Apache Spark.

    The SparkDataProcessor class provides an interface to initialize a SparkSession,
    load data into Spark DataFrames, apply various data transformations, and save
    the transformed data to specified locations. It is designed to handle operations
    such as data filtering, adding new columns, and persisting data in diverse formats.

    :ivar spark: SparkSession instance for managing operations within this class.
    :type spark: SparkSession
    """

    def __init__(self, app_name="AI_Spark_Data_Processor"):
        """
        Initialize the SparkDataProcessor with a SparkSession.
        Args:
            app_name (str): Name of the Spark Application.
        """
        self.spark = self._initialize_spark(app_name)
        print(f"Spark session initialized with app name: {app_name}")

    @staticmethod
    def _initialize_spark(app_name):
        """
        Initializes a Spark session with the specified application name.
        
        Args:
            app_name (str): Name of the Spark application.
        
        Returns:
            SparkSession: A SparkSession instance.
        """
        return SparkSession.builder \
            .appName(app_name) \
            .config("spark.master", "local") \
            .config("spark.sql.shuffle.partitions", "200") \
            .getOrCreate()

    def load_data(self, file_path, format="csv", header=True, infer_schema=True):
        """
        Load dataset into a Spark DataFrame.
        
        Args:
            file_path (str): Path to the dataset.
            format (str): Format of the file ('csv', 'parquet', 'json', etc.).
            header (bool): Whether the file contains a header row.
            infer_schema (bool): Whether to infer the schema from the data.
        
        Returns:
            DataFrame: Spark DataFrame containing the loaded data.
        """
        print(f"Loading data from {file_path} in {format} format...")
        return self.spark.read.format(format) \
            .option("header", str(header).lower()) \
            .option("inferSchema", str(infer_schema).lower()) \
            .load(file_path)

    def process_data(self, df, conditions):
        """
        Perform data transformations and filtering based on conditions.
        
        Args:
            df (DataFrame): Input Spark DataFrame.
            conditions (list of tuple): Conditions for filtering rows. Each condition should be
                                        specified as a tuple (column, operator, value).
                                        Example: [("value", ">", 50), ("category", "==", "A")]
        
        Returns:
            DataFrame: Transformed Spark DataFrame.
        """
        print("Processing data with specified transformation conditions...")
        for column, operator, value in conditions:
            if operator == ">":
                df = df.filter(col(column) > value)
            elif operator == "<":
                df = df.filter(col(column) < value)
            elif operator == "==":
                df = df.filter(col(column) == value)
            elif operator == "!=":
                df = df.filter(col(column) != value)
            else:
                raise ValueError(f"Unsupported operator: {operator}")

        return df

    def add_column(self, df, new_column_name, condition_column, threshold):
        """
        Add a new column to the DataFrame with dynamic values based on a condition.

        Args:
            df (DataFrame): The input DataFrame.
            new_column_name (str): Name of the new column to be created.
            condition_column (str): Column to apply the condition on.
            threshold (int or float): Condition threshold for generating column values.

        Returns:
            DataFrame: DataFrame with the new column added.
        """
        print(f"Adding new column '{new_column_name}' based on condition on column '{condition_column}'...")
        return df.withColumn(
            new_column_name,
            when(col(condition_column) > threshold, "high").otherwise("low")
        )

    def save_data(self, df, output_path, format="csv"):
        """
        Save the DataFrame to a specified location in a specified format.
        
        Args:
            df (DataFrame): Spark DataFrame to save.
            output_path (str): Path to save the output file.
            format (str): Format to save the data ('csv', 'parquet', 'json', etc.).
        """
        print(f"Saving data to {output_path} in {format} format...")
        df.write.format(format).mode("overwrite").save(output_path)


# Example Usage
if __name__ == "__main__":
    processor = SparkDataProcessor()

    # Load data
    input_file = "massive_dataset.csv"  # Replace with your dataset path
    data_frame = processor.load_data(file_path=input_file)

    # Perform transformations
    transformation_conditions = [("target_column", ">", 10)]
    transformed_data = processor.process_data(data_frame, transformation_conditions)

    # Add a derived column for categorization
    categorized_data = processor.add_column(
        df=transformed_data,
        new_column_name="risk_level",
        condition_column="score",
        threshold=50
    )

    # Display transformed data
    print("Displaying transformed data:")
    categorized_data.show()

    # Save the processed data to an output location
    output_file = "processed_dataset.csv"  # Replace with your output path
    processor.save_data(categorized_data, output_path=output_file)
