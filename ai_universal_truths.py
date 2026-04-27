"""
===============================================================================
AI Universal Truths
===============================================================================
The AI Universal Truths module is a lightweight and extensible knowledge base
designed to hold, manage, and reason about universal concepts and truths. This
can be used as a central component for knowledge representation in AI systems.

GitHub Repository: <https://github.com/your-repo> (Replace with your repository link)
License: MIT License (or other preferred open-source license)
Maintainer: G.O.D Framework Team
===============================================================================
"""

import logging
from typing import Dict, Any, List, Callable


class UniversalTruths:
    """
    Manages a repository of universal truths to store, query, and reason over fundamental insights.

    Provides capabilities to define, discover, retrieve, and reason about universal truths. This
    class is designed to maintain and manage a structured collection of truths while enabling logical
    reasoning operations based on user-defined rules.

    :ivar truths: Stores universal truths as key-value pairs where the keys are identifiers and
        the values are truths or insights.
    :type truths: Dict[str, str]
    :ivar logger: Logger instance used for logging operational details and errors in the system.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initializes the UniversalTruths system with predefined truths.
        """
        self.truths = {
            "laws_of_physics": "Energy cannot be created or destroyed.",
            "nature_of_time": "Time is both linear and cyclical.",
            "existence_of_love": "Love binds all things—energy, matter, consciousness."
        }
        self.logger = logging.getLogger("UniversalTruths")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger.info("UniversalTruths system initialized with predefined truths.")

    def discover_new_truth(self, new_truth: str) -> None:
        """
        Adds a new truth to the knowledge repository.

        Args:
            new_truth (str): A new universal truth or insight to append.

        Raises:
            ValueError: If the new truth is empty or already exists.
        """
        if not new_truth:
            raise ValueError("Truth cannot be empty.")

        if new_truth in self.truths.values():
            raise ValueError("This truth already exists in the system.")

        key = f"truth_{len(self.truths) + 1}"
        self.truths[key] = new_truth
        self.logger.info(f"New truth discovered and added: {key}: {new_truth}")

    def reveal_all_truths(self) -> Dict[str, str]:
        """
        Returns all universal truths stored in the system.

        Returns:
            Dict[str, str]: A collection of universal truths as key-value pairs.
        """
        self.logger.info("Revealing all stored universal truths.")
        return self.truths

    def query_truth(self, name: str) -> str:
        """
        Retrieves the definition for a specified truth.

        Args:
            name (str): The key or identifier of the truth to query.

        Returns:
            str: The value or content of the specified truth.

        Raises:
            KeyError: If the specified truth is not found in the repository.
        """
        if name not in self.truths:
            self.logger.error(f"Query failed. Truth '{name}' not found.")
            raise KeyError(f"Truth '{name}' not found in the system.")

        self.logger.info(f"Truth '{name}' retrieved successfully.")
        return self.truths[name]

    def reason_over_facts(self, rules: List[Callable[[Dict[str, Any]], bool]]) -> bool:
        """
        Performs reasoning operations over truths using logical rules.

        Args:
            rules (List[Callable[[Dict[str, Any]], bool]]): A list of lambda functions or rules that
                                                           define reasoning logic.
        
        Returns:
            bool: The outcome of the logical reasoning (True if all rules are satisfied).

        Raises:
            Exception: If an error occurs during reasoning.
        """
        self.logger.info("Starting reasoning process using provided rules.")
        try:
            results = [rule(self.truths) for rule in rules]
            is_all_rules_met = all(results)
            self.logger.info(f"Reasoning completed. All rules satisfied: {is_all_rules_met}")
            return is_all_rules_met
        except Exception as e:
            self.logger.error(f"Reasoning operation failed: {e}")
            raise


if __name__ == "__main__":
    """
    Example usage of UniversalTruths
    """
    # Initialize the truth system
    truth_keeper = UniversalTruths()

    # Retrieve and display all predefined truths
    print("Predefined Universal Truths:")
    for key, value in truth_keeper.reveal_all_truths().items():
        print(f"{key}: {value}")

    # Add a new truth
    new_truth = "Every atom contains infinite potential."
    try:
        truth_keeper.discover_new_truth(new_truth)
        print("\nNew truth added.")
    except ValueError as e:
        print(f"Failed to add truth: {e}")

    # Retrieve and display updated truths
    print("\nUpdated Universal Truths:")
    for key, value in truth_keeper.reveal_all_truths().items():
        print(f"{key}: {value}")

    # Query a specific truth
    try:
        queried_truth = truth_keeper.query_truth("laws_of_physics")
        print(f"\nQueried Truth - laws_of_physics: {queried_truth}")
    except KeyError as e:
        print(f"Query Error: {e}")

    # Perform reasoning over truths
    print("\nPerforming logical reasoning...")
    rules = [
        lambda truths: truths["laws_of_physics"] == "Energy cannot be created or destroyed.",
        lambda truths: "existence_of_love" in truths
    ]
    reasoning_result = truth_keeper.reason_over_facts(rules)
    print(f"Logical reasoning outcome: {reasoning_result}")