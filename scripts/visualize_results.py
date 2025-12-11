import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------
# Example inputs (replace with your data)
# ----------------------------------
scenarios = ["Wait Time", "Ski Time", "Lift Time"]

# Dictionary keyed by metric name
# Each metric has a list of (mean, lower_CI, upper_CI) for each scenario
metrics = {
    "Baseline": [
        (90.1, 83.21, 96.98),
        (82.62, 80.58, 84.67),
        (105.74, 103.51, 107.97)
    ],
    "Lift E Speed Upgrade": [
        (60.76, 49.18, 72.34),
        (93.89, 89.97, 97.82),
        (111.56, 107.86, 115.26)
    ],
    "Lift E Capacity Upgrade": [
        (52.53, 47.01, 58.06),
        (94.01, 92.41, 95.61),
        (119.83, 118.63, 121.03)
    ]
}

# ----------------------------------
# Plot
# ----------------------------------
num_metrics = len(metrics)
num_scenarios = len(scenarios)

x = np.arange(num_scenarios)  # scenario positions
width = 0.4 / num_metrics     # width of each metric's "column"

plt.figure(figsize=(12, 6))

for i, (metric_name, values) in enumerate(metrics.items()):
    means = np.array([v[0] for v in values])
    lower = np.array([v[1] for v in values])
    upper = np.array([v[2] for v in values])

    # Confidence interval size around the mean
    yerr = np.vstack([means - lower, upper - means])

    # Offset groups so metrics do not overlap
    offset = (i - (num_metrics - 1) / 2) * width

    plt.errorbar(
        x + offset,
        means,
        yerr=yerr,
        fmt='o',
        capsize=4,
        label=metric_name,
    )

# ----------------------------------
# Styling
# ----------------------------------
plt.xticks(x, scenarios)
plt.xlabel("Metrics")
plt.ylabel("Mean Value")
plt.title("Ski Simulation Results with 95% Confidence Intervals")
plt.legend(title="Scenarios")
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig('results_graph.png')