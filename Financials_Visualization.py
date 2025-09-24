import matplotlib.pyplot as plt
import numpy as np

# Data
fy = ['FY23', 'FY24', 'FY25']
equity = np.array([102, 338, 360])
debt = np.array([173.12, 189.52, 353.29])
net_revenue = np.array([16, 32, 49])
ebitda_pct = np.array([-92, -45, -5])
pat_pct = np.array([-105, -44, -9])

# X positions
x = np.arange(len(fy))
width = 0.35  # width of bars

fig, ax1 = plt.subplots(figsize=(10,6))

# Stacked bars: Equity + Debt
stacked_bars = ax1.bar(x, equity, width, color='navy')
ax1.bar(x, debt, width, bottom=equity, color='skyblue')

# Clustered bar for Net Revenue (offset)
revenue_bars = ax1.bar(x + width, net_revenue, width, color='green')

# Primary y-axis label
ax1.set_ylabel('Amount (Cr)')
ax1.set_xticks(x + width/2)
ax1.set_xticklabels(fy)

# Secondary y-axis for percentages
ax2 = ax1.twinx()
ebitda_line, = ax2.plot(x + width/2, ebitda_pct, color='orange', marker='o', label='EBITDA %')
pat_line, = ax2.plot(x + width/2, pat_pct, color='green', marker='s', label='PAT %')
ax2.set_ylabel('Percentage (%)')

# Custom legend
ax1.legend([stacked_bars, revenue_bars, ebitda_line],
           ['Equity + Debt', 'Net Revenue', 'EBITDA %'],
           loc='upper left')

plt.title('Financial Overview')
plt.show()
