import matplotlib.pyplot as plt

def graphPlot(algorithms, faults):
    """
    Plots the bars on the ACTIVE figure.
    Does not create a new figure or save it.
    """
    # Create bars
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = plt.bar(algorithms, faults, color=colors[:len(algorithms)])
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(faults[i])}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')
    
    # Customize plot
    plt.xlabel("Page Replacement Algorithms", fontsize=14, fontweight='bold')
    plt.ylabel("Number of Page Faults", fontsize=14, fontweight='bold')
    plt.title("Algorithm Comparison - Page Faults", fontsize=16, fontweight='bold')
    
    # Add grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Set y-axis to start from 0
    if faults:
        plt.ylim(0, max(faults) * 1.2)
    
    return plt