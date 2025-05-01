"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np


class ClusteringService:
    """
    The ClusteringService class provides tools for creating and using clustering models.

    This class allows users to initialize a clustering model with a specific algorithm, fit
    the model to input data, evaluate the clustering performance with silhouette scoring,
    and visualize the resulting clusters.

    :ivar algorithm: The clustering algorithm to be used, such as 'kmeans' or 'dbscan'.
    :type algorithm: str
    :ivar params: Additional parameters for the chosen clustering algorithm.
    :type params: dict
    :ivar model: The instantiated clustering model.
    :type model: Optional[Union[KMeans, DBSCAN]]
    """

    def __init__(self, algorithm: str = "kmeans", **kwargs):
        """
        Initialize the ClusteringService with the selected algorithm and parameters.

        :param algorithm: The clustering algorithm to use (e.g., 'kmeans', 'dbscan').
        :param kwargs: Additional parameters for the clustering algorithm.
        """
        self.algorithm = algorithm
        self.params = kwargs
        self.model = None

        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self._initialize_model()

    def _initialize_model(self):
        """
        Initialize the clustering model based on the algorithm selected during instantiation.
        """
        if self.algorithm == "kmeans":
            self.num_clusters = self.params.get("n_clusters", 3)
            self.model = KMeans(n_clusters=self.num_clusters, random_state=42)
            logging.info(f"Initialized KMeans with {self.num_clusters} clusters.")
        elif self.algorithm == "dbscan":
            eps = self.params.get("eps", 0.5)
            min_samples = self.params.get("min_samples", 5)
            self.model = DBSCAN(eps=eps, min_samples=min_samples)
            logging.info(f"Initialized DBSCAN with eps={eps}, min_samples={min_samples}.")
        else:
            raise ValueError(f"Unsupported clustering algorithm: {self.algorithm}")

    def fit(self, data: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Fit the clustering algorithm to the data and return the cluster labels and silhouette score.

        :param data: Input dataset to cluster (NumPy array).
        :return: A tuple containing (cluster_labels, silhouette_score).
        """
        logging.info("Starting clustering process...")

        # Normalize data
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(data)

        # Fit model and predict cluster labels
        cluster_labels = self.model.fit_predict(normalized_data)

        # Check if silhouette score can be computed
        if len(np.unique(cluster_labels)) > 1:
            score = silhouette_score(normalized_data, cluster_labels)
            logging.info(f"Clustering completed with silhouette score: {score:.2f}")
        else:
            score = -1  # Silhouette score is undefined for one cluster
            logging.warning("Silhouette score could not be computed (only one cluster detected).")

        logging.info(f"Clusters assigned: {list(cluster_labels)}")
        return cluster_labels, score

    def visualize_clusters(self, data: np.ndarray, labels: np.ndarray):
        """
        Visualizes data points in a 2D scatter plot with color-coded clusters.

        :param data: Input dataset (must have been normalized) for visualization (2D).
        :param labels: Cluster labels to overlay on the visualization.
        """
        plt.scatter(data[:, 0], data[:, 1], c=labels, cmap="viridis", alpha=0.7, edgecolor="k")
        plt.title(f"Cluster Visualization ({self.algorithm.capitalize()})")
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.colorbar(label="Cluster")
        plt.show()


if __name__ == "__main__":
    # Example usage
    # Generate sample dataset
    sample_data = np.array([
        [1.2, 2.3],
        [1.5, 2.5],
        [7.8, 8.1],
        [8.0, 8.3],
        [1.1, 2.2],
        [7.9, 8.2],
        [1.3, 2.1],
        [8.1, 8.4],
    ])

    # Initialize clustering service for KMeans
    clustering_service = ClusteringService(algorithm="kmeans", n_clusters=2)

    # Apply clustering
    labels, silhouette = clustering_service.fit(sample_data)
    print("Cluster Labels:", labels)
    print("Silhouette Score:", silhouette)

    # Visualize the clusters
    clustering_service.visualize_clusters(sample_data, labels)
