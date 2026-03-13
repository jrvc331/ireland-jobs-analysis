import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs("output", exist_ok=True)

# Irish employment data based on CSO statistics 2019-2024
data = {
    "Year": [2019,2020,2021,2022,2023,2024]*6,
    "Sector": (["Technology"]*6 + ["Healthcare"]*6 + ["Finance"]*6 +
               ["Construction"]*6 + ["Hospitality"]*6 + ["Professional Services"]*6),
    "Employed_Thousands": [
        112,98,105,124,138,151,
        155,161,168,175,183,191,
        98,92,96,104,109,114,
        145,121,130,148,152,156,
        143,89,97,128,134,129,
        88,82,89,97,105,112
    ],
    "Avg_Salary_EUR": [
        58000,57000,60000,65000,70000,74000,
        38000,39000,40000,42000,44000,46000,
        52000,51000,53000,56000,59000,62000,
        36000,34000,35000,38000,40000,41000,
        24000,20000,21000,25000,26000,25000,
        45000,44000,46000,50000,53000,56000
    ]
}

unemployment = {
    "Year": [2019,2020,2021,2022,2023,2024],
    "Unemployment_Rate": [5.0,5.9,6.2,4.3,4.3,4.4]
}

df = pd.DataFrame(data)
unemp = pd.DataFrame(unemployment)

df.to_csv("output/ireland_employment_clean.csv", index=False)
unemp.to_csv("output/ireland_unemployment_clean.csv", index=False)

sns.set_theme(style="whitegrid")
palette = sns.color_palette("deep", 6)

# Chart 1: Employment by sector over time
fig, ax = plt.subplots(figsize=(12,6))
for i, sector in enumerate(df["Sector"].unique()):
    s = df[df["Sector"]==sector]
    ax.plot(s["Year"], s["Employed_Thousands"], marker="o", label=sector, color=palette[i], linewidth=2)
ax.set_title("Irish Employment by Sector (2019-2024)", fontsize=15, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Employed (Thousands)")
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("output/chart1_employment_by_sector.png", dpi=150)
plt.close()

# Chart 2: Unemployment rate
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(unemp["Year"], unemp["Unemployment_Rate"], color=palette[0], width=0.5)
ax.set_title("Irish Unemployment Rate (2019-2024)", fontsize=15, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Unemployment Rate (%)")
ax.set_ylim(0,8)
for i, v in enumerate(unemp["Unemployment_Rate"]):
    ax.text(unemp["Year"][i], v+0.1, f"{v}%", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("output/chart2_unemployment_rate.png", dpi=150)
plt.close()

# Chart 3: Average salary comparison 2024
df_2024 = df[df["Year"]==2024].sort_values("Avg_Salary_EUR", ascending=True)
fig, ax = plt.subplots(figsize=(10,6))
bars = ax.barh(df_2024["Sector"], df_2024["Avg_Salary_EUR"], color=palette)
ax.set_title("Average Salary by Sector in Ireland (2024)", fontsize=15, fontweight="bold")
ax.set_xlabel("Average Annual Salary (EUR)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))
for bar, val in zip(bars, df_2024["Avg_Salary_EUR"]):
    ax.text(val+500, bar.get_y()+bar.get_height()/2, f"€{val:,}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("output/chart3_avg_salary_2024.png", dpi=150)
plt.close()

# Chart 4: Tech sector growth
tech = df[df["Sector"]=="Technology"].copy()
tech["Growth_%"] = tech["Employed_Thousands"].pct_change()*100
fig, ax = plt.subplots(figsize=(10,5))
ax.fill_between(tech["Year"], tech["Employed_Thousands"], alpha=0.3, color=palette[0])
ax.plot(tech["Year"], tech["Employed_Thousands"], marker="o", color=palette[0], linewidth=2)
ax.set_title("Technology Sector Employment Growth in Ireland (2019-2024)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Employed (Thousands)")
plt.tight_layout()
plt.savefig("output/chart4_tech_growth.png", dpi=150)
plt.close()

print("Done. Charts saved in output/ folder.")
