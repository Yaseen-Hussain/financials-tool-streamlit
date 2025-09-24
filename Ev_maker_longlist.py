import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

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

# Melt into long format
df_melt = df.melt(id_vars=["Type","Company"], 
                  value_vars=["Share 2024","Share 2025"], 
                  var_name="Year", value_name="Share")

types = df_melt["Type"].unique()
years = ["Share 2024", "Share 2025"]

# Base colormaps for each Type
type_colors = {
    "2W": plt.cm.Blues,
    "3W": plt.cm.Greens,
    "4W": plt.cm.Blues,
    "Bus/Truck": plt.cm.Greens
}

# Plot
fig, ax = plt.subplots(figsize=(12,7))
bar_width = 0.35
x = np.arange(len(types))

for i, t in enumerate(types):
    # Sort companies by 2025 share (largest first = bottom)
    order = (df_melt[(df_melt["Type"]==t) & (df_melt["Year"]=="Share 2025")]
             .sort_values("Share", ascending=False)["Company"].tolist())
    
    # Assign colors: darkest for largest, lighter for smaller
    cmap = type_colors[t]
    colors = {company: cmap(1 - idx/len(order)) for idx, company in enumerate(order)}
    
    for j, y in enumerate(years):
        subset = df_melt[(df_melt["Type"]==t) & (df_melt["Year"]==y)]
        subset = subset.set_index("Company").reindex(order).reset_index()
        
        bottom = 0
        for row in subset.itertuples():
            ax.bar(i + (j-0.5)*bar_width, row.Share, bar_width, 
                   bottom=bottom, color=colors[row.Company],
                   label=row.Company if (i==0 and j==0) else "")
            
            # Label inside
            if row.Share > 2:
                ax.text(i + (j-0.5)*bar_width, bottom + row.Share/2,
                        f"{row.Share:.1f}%", ha="center", va="center", fontsize=8, color="white")
            
            bottom += row.Share

# X-axis labels
ax.set_xticks(x)
ax.set_xticklabels(types, fontsize=11)

# Legends
year_patches = [Patch(facecolor="grey", alpha=0.5, label="Share 2024"),
                Patch(facecolor="grey", alpha=0.9, label="Share 2025")]
company_handles, company_labels = ax.get_legend_handles_labels()

first_legend = ax.legend(handles=year_patches, title="Year", loc="upper left", bbox_to_anchor=(1,1))
ax.add_artist(first_legend)
ax.legend(company_handles, company_labels, title="Companies", loc="lower left", bbox_to_anchor=(1,0))

plt.title("EV Market Share by Type (2024 vs 2025)", fontsize=14)
plt.ylabel("Market Share (%)")
plt.tight_layout()
plt.show()
