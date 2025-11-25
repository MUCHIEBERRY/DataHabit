"""
visualizer.py
-------------
Handles charts and visual representation of submission behavior.
"""

import matplotlib.pyplot as plt


class Visualizer:
    """Plots delay patterns and behavior trends."""

    def __init__(self, delays):
        if not isinstance(delays, list):
            raise TypeError("delays must be a list.")

        self.delays = delays

    def plot_timeline(self):
        if not self.delays:
            raise ValueError("Cannot plot empty data. Provide delay values first.")

        plt.figure(figsize=(10, 5))
        plt.plot(self.delays, marker="o")
        plt.title("Submission Delays Over Time")
        plt.xlabel("Task #")
        plt.ylabel("Delay (hours)")
        plt.grid(True)
        plt.show()

    def plot_distribution(self):
        if not self.delays:
            raise ValueError("Cannot plot empty data. Provide delay values first.")

        plt.figure(figsize=(8, 4))
        plt.hist(self.delays, bins=10)
        plt.title("Delay Distribution")
        plt.xlabel("Delay (hours)")
        plt.ylabel("Frequency")
        plt.show()
