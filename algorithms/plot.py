import matplotlib.pyplot as plt
import numpy as np

def graphPlot(algorithms, faults):
    x = np.array(algorithms)
    y = np.array(faults)

    plt.xlabel("Page Replacement Algorithms")
    plt.ylabel("No. of Page Faults")

    plt.title("Algorithm Visualization")
    plt.grid(True)

