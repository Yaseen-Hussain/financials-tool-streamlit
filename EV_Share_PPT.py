import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data
data = {
    "Type": ["2W","2W","2W","2W",
             "3W","3W","3W","3W",
             "4W","4W","4W","4W",
             "Bus/Truck","Bus/Truck","Bus/Truck","Bus/Truck","Bus/Truck"],
    "Company": ["OLA","TVS","BAJAJ","ATHER",
                "MAHINDRA","YC ELECTRIC","BAJAJ","SAERA ELECTRIC",
                "TATA EV","JSW MG","MAHINDRA","TATA MOTORS",
                "TATA MOTORS","OLECTRA","JBM","PMI ELECTRO","SWITCH"],
    "Share 2024": [35.47,19.21,16.85,10.99,
                   9.62,6.36,6.06,4.09,
                   57.83,20.60,6.77,4.30,
                   35.64,16.55,13.94,13.02,5.46],
    "Share 2025": [18.57,23.39,21.31,14.31,
                   11.48,5.68,9.62,3.38,
                   36.59,29.97,2.37,2.06,
                   6.46,18.00,15.47,20.60,21.13]
}

df = pd.DataFrame(data)

# Prepare
df_melt = df.melt(id_vars=["Type","Company"], 
                  value_vars=["Share 2024","Share 2025"], 
                  var_name="Year", value_name="Share")

pivot = df_melt.pivot_table(index=["Type","Year"], 
                            columns="Company", 
                            values="Share", 
                            fill_value=0)

# Assign simple colors for each Type
type_colors = {
    "2W": "steelblue",
    "3W": "seagreen",
    "4W": "darkorange",
    "Bus/Truck": "firebrick"
}

# Plot
fig, ax = plt.subplots(figsize=(10,6))

x = np.arange(len(pivot.index))  # positions
width = 0.6

# Stacked bars per type
for i, (idx, row) in enumerate(pivot.iterrows()):
    base = 0
    color = type_colors[idx[0]]
    ax.bar(i, row.sum(), width, bottom=0, color=color, alpha=0.7, label=idx[0] if f"{idx[0]}-{idx[1]}" not in ax.get_legend_handles_labels()[1] else "")

# Labels
ax.set_xticks(x)
ax.set_xticklabels([f"{t[0]}-{t[1].split()[1]}" for t in pivot.index], rotation=45, ha="right")

plt.ylabel("Market Share (%)")
plt.title("EV Market Share by Type (2024 vs 2025)")
plt.legend(title="Type")
plt.tight_layout()
plt.show()
