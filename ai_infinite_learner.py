"""
AI Infinite Learner
====================

The Infinite Learner framework allows AI systems to accumulate, organize, and recall knowledge dynamically.
It offers a foundation for creating highly scalable knowledge-based systems with unlimited growth potential.

License: MIT
Author: G.O.D Team

Features:
---------
1. Dynamic and topic-wise knowledge management.
2. Scalable design for infinite knowledge storage.
3. Extensible and customizable base framework.
4. Includes examples for usage and advanced extensions.
"""

import json


class InfiniteLearner:
    """
    Represents a conceptual entity that can infinitely learn and recall knowledge.

    This class provides mechanisms for managing a knowledge base where information can
    be learned (added) under specific topics and recalled later. It is designed for
    dynamic expansion of topics and their corresponding knowledge entries over time.

    :ivar knowledge_base: Stores the knowledge organized by topics. Each topic maps to
                          a list of knowledge entries.
    :type knowledge_base: dict
    """

    def __init__(self):
        """
        Initializes the InfiniteLearner with an empty knowledge base.
        """
        self.knowledge_base = {}

    def learn(self, topic, knowledge):
        """
        Adds knowledge under a specific topic.

        :param topic: The subject/area of learning.
        :param knowledge: The specific data, insight, or fact to store.
        """
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = []
        self.knowledge_base[topic].append(knowledge)

    def recall(self, topic):
        """
        Retrieves the knowledge under the given topic.

        :param topic: The subject to retrieve knowledge about.
        :return: List of knowledge items under the topic, or a message if nothing is found.
        """
        return self.knowledge_base.get(topic, "Nothing learned yet.")


class SummarizingLearner(InfiniteLearner):
    """
    SummarizingLearner is a specialized extension of InfiniteLearner.

    This class provides the capability to summarize and format knowledge
    learned under specific topics. It leverages the recall method and
    presents the retrieved information in a clear, readable format.

    :ivar attribute1: Description of attribute1.
    :type attribute1: type
    :ivar attribute2: Description of attribute2.
    :type attribute2: type
    """

    def summarize_recall(self, topic):
        """
        Summarizes and formats all knowledge learned under a topic.

        :param topic: The subject of focus.
        :return: A formatted string summarizing the topic's knowledge.
        """
        knowledge = self.recall(topic)
        if isinstance(knowledge, list):
            return f"In {topic}, the following knowledge is stored:\n- " + "\n- ".join(knowledge)
        return knowledge


class PrioritizedLearner(InfiniteLearner):
    """
    Provides functionality for prioritized learning where access frequency
    of topics is tracked, enabling retrieval of the most accessed topic.

    This class inherits from the InfiniteLearner class and enhances it by
    maintaining a usage count to record how often each topic is recalled.
    It can be used in scenarios where prioritizing frequently accessed
    knowledge is important.

    :ivar usage_count: Tracks the number of times a topic is accessed.
    :type usage_count: dict
    """

    def __init__(self):
        super().__init__()
        self.usage_count = {}

    def learn(self, topic, knowledge):
        """
        Adds knowledge to the system and initializes its usage count.

        :param topic: Subject of knowledge.
        :param knowledge: Knowledge to be saved.
        """
        super().learn(topic, knowledge)
        self.usage_count[topic] = self.usage_count.get(topic, 0)

    def recall(self, topic):
        """
        Retrieves the knowledge while tracking the number of times a topic is accessed.

        :param topic: Subject to retrieve knowledge for.
        :return: Knowledge under the topic.
        """
        self.usage_count[topic] = self.usage_count.get(topic, 0) + 1
        return super().recall(topic)

    def get_most_accessed_topic(self):
        """
        Retrieves the topic which has been accessed the most.

        :return: Topic with the highest recall count or an appropriate message.
        """
        if not self.usage_count:
            return "No topics have been accessed yet."
        return max(self.usage_count, key=self.usage_count.get)


class PersistentLearner(InfiniteLearner):
    """
    Extends the functionality of InfiniteLearner by introducing the ability
    to persist and retrieve knowledge using JSON files.

    This class provides methods to save the current knowledge base to a file
    and to load it back from the file. The functionality allows long-term
    storage and retrieval of knowledge, enhancing usability and ensuring
    knowledge is not lost between sessions.

    :ivar knowledge_base: Stores the accumulated knowledge.
    :type knowledge_base: dict
    """

    def save_knowledge(self, file_name):
        """
        Saves the current knowledge base to a JSON file.

        :param file_name: The name of the file to save the knowledge base in.
        """
        with open(file_name, 'w') as file:
            json.dump(self.knowledge_base, file)
        return f"Knowledge saved to {file_name}"

    def load_knowledge(self, file_name):
        """
        Loads the knowledge base from a JSON file.

        :param file_name: The name of the file to load the knowledge base from.
        """
        try:
            with open(file_name, 'r') as file:
                self.knowledge_base = json.load(file)
            return f"Knowledge loaded from {file_name}"
        except FileNotFoundError:
            return f"File {file_name} not found."


# ===== Examples =====
if __name__ == "__main__":
    print("\n-- Example 1: Basic Infinite Learner --")
    learner = InfiniteLearner()
    learner.learn("physics", "Laws of motion.")
    learner.learn("physics", "Quantum mechanics insights.")
    print("Physics Knowledge:", learner.recall("physics"))

    print("\n-- Example 2: Summarizing Learner --")
    summarizer = SummarizingLearner()
    summarizer.learn("biology", "Evolution theory.")
    summarizer.learn("biology", "Cell structure and function.")
    print(summarizer.summarize_recall("biology"))

    print("\n-- Example 3: Prioritized Learner --")
    prioritizer = PrioritizedLearner()
    prioritizer.learn("math", "Pythagoras theorem.")
    prioritizer.learn("philosophy", "Existentialism.")
    prioritizer.recall("math")
    prioritizer.recall("math")
    prioritizer.recall("philosophy")
    print("Most accessed topic:", prioritizer.get_most_accessed_topic())

    print("\n-- Example 4: Persistent Learner --")
    persistent = PersistentLearner()
    persistent.learn("history", "The Renaissance period.")
    save_message = persistent.save_knowledge("knowledge.json")
    print(save_message)

    new_persistent = PersistentLearner()
    load_message = new_persistent.load_knowledge("knowledge.json")
    print(load_message)
    print("Recalled History Knowledge:", new_persistent.recall("history"))