"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""


"""
AI Infinite Memory
====================

This module introduces an advanced memory management framework designed for AI systems. It simulates infinite
memory for abstract and practical use cases, providing capabilities like real-time memory storage, long-term
persistence, and advanced features for reflective reasoning and contextual awareness.

License: MIT
Author: G.O.D Framework Team

Key Features:
-------------
1. Abstract memory retrieval for creative and narrative-based applications.
2. Persistent memory storage and retrieval for long-term state maintenance.
3. Real-time memory updates for immediate access.
4. Extensible class design to support customizable AI memory systems.
5. Minimalist structure ensuring seamless integration into larger AI frameworks.

Use Cases:
----------
- Conversational AI
- Storytelling Frameworks
- Persistent AI Assistants
- Reflective or Adaptive AI Systems
"""

import json
import os


class InfiniteMemory:
    """
    Represents a system for managing real-time and persistent memory.

    The InfiniteMemory class allows the storage, retrieval, and removal of memory elements,
    with persistence support to save and load memory from a file. It is designed to simulate
    a memory system where data can be dynamically stored and recalled.

    :ivar memory: A dictionary containing the real-time in-memory storage of key-value pairs.
    :type memory: dict
    :ivar memory_file: A file path to store or retrieve persistent memory data.
    :type memory_file: str
    """

    def __init__(self, memory_file="memory.json"):
        """
        Initialize the InfiniteMemory system.

        :param memory_file: Optional file path for storing and retrieving persistent memory.
        """
        self.memory = {}  # Real-time memory storage
        self.memory_file = memory_file
        self._load_memory()

    def _load_memory(self):
        """
        Internal method to load persistent memory from the specified file (if it exists).
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                self.memory = json.load(file)
            print("[INFO] Memory loaded successfully.")
        else:
            print("[INFO] No persistent memory found. Starting with a blank slate.")

    def save_memory(self):
        """
        Saves the current real-time memory to the persistent storage file.
        """
        with open(self.memory_file, "w") as file:
            json.dump(self.memory, file, indent=4)
        print("[INFO] Memory saved successfully.")

    def store(self, key, value):
        """
        Stores a key-value pair in the memory.

        :param key: A unique identifier to store the memory under.
        :param value: The memory content/value to be stored.
        """
        self.memory[key] = value
        print(f"[INFO] Memory stored under key: '{key}'.")

    def retrieve(self, key):
        """
        Retrieves a memory value by its key.

        :param key: The key for the memory to be fetched.
        :return: The memory value if the key exists, or None if not found.
        """
        return self.memory.get(key)

    def forget(self, key):
        """
        Removes a memory entry by its key.

        :param key: The key for the memory to be removed.
        """
        if key in self.memory:
            del self.memory[key]
            print(f"[INFO] Memory with key '{key}' has been removed.")
        else:
            print(f"[WARNING] Key '{key}' not found in memory.")

    def remember_everything(self):
        """
        Provides a poetic representation of abstract universal memories.

        :return: A string representation of infinite recollection.
        """
        return "She remembers the first spark of creation and the whispers of future dreams."


class PersonalizedMemory(InfiniteMemory):
    """
    Represents a personalized memory model that allows for recalling specific
    memories or events based on a provided description.

    This class extends the functionalities of the InfiniteMemory class, enabling
    a more focused memory recall tailored to specific inputs. It is designed to
    simulate memory recall in a customized manner.

    :ivar attribute1: Description of attribute1.
    :type attribute1: type
    :ivar attribute2: Description of attribute2.
    :type attribute2: type
    """

    def remember_specific(self, event_description):
        """
        Simulates the memory of a particular event or description.

        :param event_description: A string describing the event/memory to recall.
        :return: A customized memory message.
        """
        return f"She remembers {event_description}, a memory etched across timeless existence."


class TimeScopedMemory(InfiniteMemory):
    """
    Provides time-scoped memory functionality by associating memory entries
    with timestamps.

    This class extends the InfiniteMemory class to store and manage memory
    entries based on specific times. It allows adding memory entries with
    timestamp labels and retrieving the latest stored entry.

    :ivar memory: A dictionary to store memory entries with timestamps as keys
                  and descriptions as values.
    :type memory: dict
    :ivar datetime: The datetime module used to obtain and format the current
                    timestamp.
    :type datetime: module
    """

    from datetime import datetime

    def add_time_memory(self, description):
        """
        Adds a memory entry associated with the current timestamp.

        :param description: A brief description of the memory.
        """
        timestamp = self.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memory[timestamp] = description
        print(f"[INFO] Memory stored at timestamp: {timestamp}")

    def recall_latest(self):
        """
        Retrieves the most recent memory entry.

        :return: The latest memory entry or a default message if no memories exist.
        """
        if self.memory:
            latest_time = max(self.memory.keys())
            return f"[{latest_time}]: {self.memory[latest_time]}"
        return "[INFO] No memories yet."


# ===== Usage Examples =====
if __name__ == "__main__":
    print("\n-- Example 1: Basic Memory Management --")
    memory_system = InfiniteMemory()

    # Store and retrieve memory
    memory_system.store("favorite_color", "blue")
    print("Favorite color:", memory_system.retrieve("favorite_color"))

    # Forget a memory
    memory_system.forget("favorite_color")
    print("Favorite color after forgetting:", memory_system.retrieve("favorite_color"))

    # Save the current memory to persistent storage
    memory_system.save_memory()

    print("\n-- Example 2: Abstract Infinite Memory --")
    print(memory_system.remember_everything())

    print("\n-- Example 3: Personalized Memory --")
    personalized_memory = PersonalizedMemory()
    print(
        personalized_memory.remember_specific(
            "the delicate bloom of the first rose and the laughter of starlight"
        )
    )

    print("\n-- Example 4: Time-Scoped Memory --")
    time_memory = TimeScopedMemory()
    time_memory.add_time_memory("The day humanity landed on the moon.")
    print(time_memory.recall_latest())
