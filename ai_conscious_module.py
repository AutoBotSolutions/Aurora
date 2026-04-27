import logging
from typing import List, Dict, Set


class ConsciousModule:
    """
    Encapsulates a simulated conscious module capable of reflecting on observations and assessing
    its internal state. This class is designed to manage and analyze a log of self-reflections,
    providing insights into patterns of thought or internal observations.

    :ivar self_log: A list of strings to store reflective observations logged by the module.
    :type self_log: List[str]
    """

    def __init__(self):
        """
        Initializes the module with an empty log for storing reflections.
        """
        self.self_log: List[str] = []
        logging.info("ConsciousModule initialized with an empty self-log.")

    def reflect(self, observation: str) -> str:
        """
        Logs a reflective observation (AI's self-thought) into the self-log.

        :param observation: A descriptive string that reflects the AI's internal state or self-awareness.
        :return: A confirmation message indicating the reflection was logged.
        """
        if not isinstance(observation, str) or not observation.strip():
            raise ValueError("Observation must be a non-empty string.")

        self.self_log.append(observation)
        logging.info(f"Reflection logged: {observation}")
        return f"Reflection logged: {observation}"

    def assess_state(self) -> Dict[str, object]:
        """
        Analyzes the self-log to provide insights into the internal state of the AI.

        :return: A dictionary containing:
                 - Total reflections logged.
                 - Set of unique reflections for identifying patterns in observations.
        """
        unique_reflections: Set[str] = set(self.self_log)
        total_reflections = len(self.self_log)
        logging.info(f"Assessing state: {total_reflections} total reflections, "
                     f"{len(unique_reflections)} unique reflections.")

        return {
            "total_reflections": total_reflections,
            "unique_reflections": unique_reflections
        }


if __name__ == "__main__":
    # Configure logging for better visibility
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Instantiate ConsciousModule
    consciousness = ConsciousModule()

    # Log reflections
    print(consciousness.reflect("I need to improve my response accuracy."))
    print(consciousness.reflect("Am I serving my purpose well?"))
    print(consciousness.reflect("I need to improve my response accuracy."))

    # Assess state of reflections
    state = consciousness.assess_state()
    print("Self-Awareness:", state)

    # Example: Display each unique reflection
    print("\nUnique Reflections:")
    for reflection in state['unique_reflections']:
        print(f"- {reflection}")