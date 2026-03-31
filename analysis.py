import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs("output", exist_ok=True)

# Load real CSO data
df = pd.read_csv("/Users/apple/Desktop/My Folder/WorkSpace/NAQ09.20260331T160304.csv")

# Clean and filter
df = df[df["Employment Status"] == "All persons in employment"]
df["Year"] = df["Quarter"].str[:4].astype(int)
df = df[df["Year"] >= 2019]
df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")

# Focus on key sectors
sectors = [
    "Information and Communication",
    "Human Health and Social Work Activities",
    "Financial and Insurance Activities",
    "Construction",
    "Distribution, Transport, Hotels and Restaurants",
    "Professional, Scientific and Technical Activities"
]
df = df[df["NACE Rev. 2 Sector"].isin(sectors)]

# Annual average
annual = df.groupby(["Year", "NACE Rev. 2 Sector"])["VALUE"].mean().reset_index()
annual.columns = ["Year", "Sector", "Employed_Thousands"]

# Short sector names for charts
short_names = {
    "Information and Communication": "Tech/ICT",
    "Human Health and Social Work Activities": "Healthcare",
    "Financial and Insurance Activities": "Finance",
    "Construction": "Construction",
    "Distribution, Transport, Hotels and Restaurants": "Distribution/Hospitality",
    "Professional, Scientific and Technical Activities": "Professional Services"
}
annual["Sector"] = annual["Sector"].map(short_names)

# Save clean CSV
annual.to_csv("output/ireland_employment_clean.csv", index=False)

sns.set_theme(style="whitegrid")
palette = sns.color_palette("deep", 6)

# Chart 1: Employment by sector over time
fig, ax = plt.subplots(figsize=(12,6))
for i, sector in enumerate(annual["Sector"].unique()):
    s = annual[annual["Sector"]==sector]
    ax.plot(s["Year"], s["Employed_Thousands"], marker="o", label=sector, color=palette[i], linewidth=2)
ax.set_title("Irish Employment by Sector (2019-2024)", fontsize=15, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Employed (Thousands)")
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("output/chart1_employment_by_sector.png", dpi=150)
plt.close()

# Chart 2: 2024 employment comparison
latest = annual[annual["Year"]==2024].sort_values("Employed_Thousands", ascending=True)
fig, ax = plt.subplots(figsize=(10,6))
bars = ax.barh(latest["Sector"], latest["Employed_Thousands"], color=palette)
ax.set_title("Employment by Sector in Ireland (2024)", fontsize=15, fontweight="bold")
ax.set_xlabel("Employed (Thousands)")
for bar, val in zip(bars, latest["Employed_Thousands"]):
    ax.text(val+1, bar.get_y()+bar.get_height()/2, f"{val:.1f}k", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("output/chart2_sector_comparison_2024.png", dpi=150)
plt.close()

# Chart 3: ICT sector growth
tech = annual[annual["Sector"]=="Tech/ICT"].copy()
fig, ax = plt.subplots(figsize=(10,5))
ax.fill_between(tech["Year"], tech["Employed_Thousands"], alpha=0.3, color=palette[0])
ax.plot(tech["Year"], tech["Employed_Thousands"], marker="o", color=palette[0], linewidth=2)
ax.set_title("Tech/ICT Sector Employment Growth in Ireland (2019-2024)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Employed (Thousands)")
plt.tight_layout()
plt.savefig("output/chart3_tech_growth.png", dpi=150)
plt.close()

# Chart 4: % growth since 2019
base = annual[annual["Year"]==2019][["Sector","Employed_Thousands"]].set_index("Sector")
latest2 = annual[annual["Year"]==2024][["Sector","Employed_Thousands"]].set_index("Sector")
growth = ((latest2 - base) / base * 100).reset_index()
growth.columns = ["Sector", "Growth_%"]
growth = growth.sort_values("Growth_%", ascending=True)
fig, ax = plt.subplots(figsize=(10,6))
colors = [palette[0] if x >= 0 else palette[3] for x in growth["Growth_%"]]
ax.barh(growth["Sector"], growth["Growth_%"], color=colors)
ax.set_title("Employment Growth by Sector: 2019 vs 2024 (%)", fontsize=14, fontweight="bold")
ax.set_xlabel("Growth (%)")
ax.axvline(0, color="black", linewidth=0.8)
for i, val in enumerate(growth["Growth_%"]):
    ax.text(val+0.3, i, f"{val:.1f}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("output/chart4_growth_comparison.png", dpi=150)
plt.close()

print("Done. Real CSO data analysed. Charts saved in output/ folder.")
