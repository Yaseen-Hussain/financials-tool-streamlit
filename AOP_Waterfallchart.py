import matplotlib.pyplot as plt
import numpy as np

# Data
companies = ["First Energy", "Ampin", "K Raheja", "BN Energy Module", "BN Energy BOS", "Total"]
value_ebitda = [100.44, 45.08, 71.28, 131.32, 129.72, 477.84]
ebitda = [7.56, 3.92, 9.72, 2.68, 8.28, 32.16]

# Compute cumulative base for waterfall effect
value_base = [0] + list(np.cumsum(value_ebitda[:-1]))

# For EBITDA, stack it on top of Value-EBITDA
ebitda_bottom = [v + e for v, e in zip(value_base, [0]+ebitda[:-1])]

# Plot
fig, ax = plt.subplots(figsize=(10,6))

# Plot Value-EBITDA
ax.bar(companies, value_ebitda, bottom=value_base, color='royalblue', label='Value-EBITDA')

# Plot EBITDA on top of Value-EBITDA
ax.bar(companies, ebitda, bottom=ebitda_bottom, color='green', label='EBITDA')

# Add value labels
for i in range(len(companies)):
    # Value-EBITDA label
    ax.text(i, value_base[i] + value_ebitda[i]/2, f'{value_ebitda[i]:.2f}', ha='center', color='white', fontsize=10)
    # EBITDA label
    ax.text(i, ebitda_bottom[i] + ebitda[i]/2, f'{ebitda[i]:.2f}', ha='center', color='white', fontsize=10)

# Customize
ax.set_title("Stacked Waterfall: Value-EBITDA + EBITDA")
ax.set_ylabel("Amount")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
